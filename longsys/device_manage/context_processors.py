def get_msg(request):
    """ 获取用户信息"""
    ip = request.META.get('REMOTE_ADDR')
    name = request.session.get('name')
    job = request.session.get('job')
    is_admin = request.session.get('is_admin')
    is_init = request.session.get('is_init')
    staff_number = request.session.get('staff_number')
    if name is None:
        name = '客户'
        job = '客户'
        is_admin = False
        is_init = False
    return {
        'name': name,
        'job': job,
        'is_admin': 1 if is_admin else 0,
        'is_init': 1 if is_init else 0,
        'staff_number': staff_number,
        'ip': ip,
    }
