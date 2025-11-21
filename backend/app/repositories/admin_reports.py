from typing import List, Tuple
from pymysql.cursors import DictCursor


def _duration_filters(duration_months: int):
    """Helper: return tuple(duration_months, duration_days, name_like)"""
    duration_days = duration_months * 30
    duration_name_like = f"%{duration_months}개월%"
    return duration_months, duration_days, duration_name_like


def get_members_by_membership_duration(
    cursor: DictCursor,
    duration_months: int,
    status: str = "all",
    skip: int = 0,
    limit: int = 100,
) -> Tuple[List[dict], int]:
    """
    회원권(duration_months)을 가진 모든 회원 또는 만료된 회원만 조회.
    status: 'all' or 'expired'
    returns: (rows, total)
    """
    dm, dd, name_like = _duration_filters(duration_months)

    base_where = "m.is_active = TRUE"
    type_where = "(mt.duration_months = %s OR mt.duration_days = %s OR mt.name LIKE %s)"

    params = [dm, dd, name_like]

    expiry_where = ""
    if status == "expired":
        expiry_where = "AND (m.membership_end_date IS NOT NULL AND m.membership_end_date < CURDATE())"

    where_clause = f"{base_where} AND {type_where} {expiry_where}"

    count_sql = f"""
    SELECT COUNT(*) as total
    FROM members m
    JOIN membership_types mt ON m.membership_type_id = mt.id
    WHERE {where_clause}
    """
    cursor.execute(count_sql, tuple(params))
    total = cursor.fetchone().get("total", 0)

    sql = f"""
    SELECT
        m.member_id,
        m.name,
        m.phone_number,
        mt.name as membership_type_name,
        mt.duration_months,
        m.membership_start_date,
        m.membership_end_date,
        CASE WHEN m.membership_end_date IS NULL THEN 'active' WHEN m.membership_end_date < CURDATE() THEN 'expired' ELSE 'active' END as status
    FROM members m
    JOIN membership_types mt ON m.membership_type_id = mt.id
    WHERE {where_clause}
    ORDER BY m.membership_end_date DESC
    LIMIT %s OFFSET %s
    """

    params.extend([limit, skip])
    cursor.execute(sql, tuple(params))
    rows = cursor.fetchall()
    return rows, total


def get_uniform_rentals_by_duration(
    cursor: DictCursor,
    duration_months: int = None,
    status: str = "all",
    skip: int = 0,
    limit: int = 100,
) -> Tuple[List[dict], int]:
    """
    유니폼(회원복) 렌탈권을 가진 회원 조회.
    duration_months: optional - 회원권 기간 기반 필터
    status: 'all' or 'expired' (렌탈 만료)
    """
    params = []
    where_parts = ["1=1"]

    if duration_months:
        dm, dd, name_like = _duration_filters(duration_months)
        where_parts.append("(mt.duration_months = %s OR mt.duration_days = %s OR mt.name LIKE %s)")
        params.extend([dm, dd, name_like])

    if status == "expired":
        where_parts.append("(u.rental_end_date IS NOT NULL AND u.rental_end_date < CURDATE())")

    where_sql = " AND ".join(where_parts)

    count_sql = f"""
    SELECT COUNT(DISTINCT u.member_id) as total
    FROM uniform_rentals u
    JOIN members m ON u.member_id = m.member_id
    LEFT JOIN membership_types mt ON m.membership_type_id = mt.id
    WHERE {where_sql}
    """
    cursor.execute(count_sql, tuple(params))
    total = cursor.fetchone().get("total", 0)

    sql = f"""
    SELECT
        u.id as rental_id,
        u.member_id,
        m.name,
        m.phone_number,
        u.rental_start_date,
        u.rental_end_date,
        u.rental_type,
        mt.name as membership_type_name,
        CASE WHEN u.rental_end_date IS NULL THEN 'active' WHEN u.rental_end_date < CURDATE() THEN 'expired' ELSE 'active' END as rental_status
    FROM uniform_rentals u
    JOIN members m ON u.member_id = m.member_id
    LEFT JOIN membership_types mt ON m.membership_type_id = mt.id
    WHERE {where_sql}
    GROUP BY u.id
    ORDER BY u.rental_end_date DESC
    LIMIT %s OFFSET %s
    """

    params.extend([limit, skip])
    cursor.execute(sql, tuple(params))
    rows = cursor.fetchall()
    return rows, total


def get_locker_rentals_by_duration(
    cursor: DictCursor,
    duration_months: int = None,
    status: str = "all",
    skip: int = 0,
    limit: int = 100,
) -> Tuple[List[dict], int]:
    """
    라커룸 렌탈권을 가진 회원 조회.
    duration_months: optional - 회원권 기간 기반 필터
    status: 'all' or 'expired'
    """
    params = []
    where_parts = ["1=1"]

    if duration_months:
        dm, dd, name_like = _duration_filters(duration_months)
        where_parts.append("(mt.duration_months = %s OR mt.duration_days = %s OR mt.name LIKE %s)")
        params.extend([dm, dd, name_like])

    if status == "expired":
        where_parts.append("(l.rental_end_date IS NOT NULL AND l.rental_end_date < CURDATE())")

    where_sql = " AND ".join(where_parts)

    count_sql = f"""
    SELECT COUNT(DISTINCT l.member_id) as total
    FROM locker_rentals l
    JOIN members m ON l.member_id = m.member_id
    LEFT JOIN membership_types mt ON m.membership_type_id = mt.id
    WHERE {where_sql}
    """
    cursor.execute(count_sql, tuple(params))
    total = cursor.fetchone().get("total", 0)

    sql = f"""
    SELECT
        l.id as rental_id,
        l.member_id,
        m.name,
        m.phone_number,
        l.locker_number,
        l.rental_start_date,
        l.rental_end_date,
        l.rental_type,
        mt.name as membership_type_name,
        CASE WHEN l.rental_end_date IS NULL THEN 'active' WHEN l.rental_end_date < CURDATE() THEN 'expired' ELSE 'active' END as rental_status
    FROM locker_rentals l
    JOIN members m ON l.member_id = m.member_id
    LEFT JOIN membership_types mt ON m.membership_type_id = mt.id
    WHERE {where_sql}
    ORDER BY l.rental_end_date DESC
    LIMIT %s OFFSET %s
    """

    params.extend([limit, skip])
    cursor.execute(sql, tuple(params))
    rows = cursor.fetchall()
    return rows, total
