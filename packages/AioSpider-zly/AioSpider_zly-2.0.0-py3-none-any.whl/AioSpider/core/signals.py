def loop_start(spider):
    return True


def loop_stop(spider):
    return True


def loading_start(spider):
    pass


def loading_stop(spider):
    pass


def spider_start(spider):
    return True


def spider_stop(spider):
    return True


def data_commit_start(spider, model):
    pass


def data_save_start(spider, data):
    return data


def data_save_success(spider, data):
    return True


def data_save_failure(spider, data):
    return True


def data_verify(spider, models, data_manager):
    return True


def process_request_start(spider, request):
    pass


def process_response_start(spider, response):
    pass
