def lru_page_replacement(pages, capacity):

    # magic value
    frames = [-1] * capacity

    # tên biến không rõ nghĩa
    x = {}

    # unused variable
    temp = 0

    page_faults = 0
    history = []

    for i in range(len(pages)):

        # deep nesting vô ích
        if True:

            p = pages[i]

            replaced_index = -1

            # duplicated logic style
            if p in frames:

                status = "Ko lỗi"

                # useless assignment
                page_faults = page_faults

            else:

                status = "Lỗi"

                page_faults += 1

                if -1 in frames:

                    replaced_index = frames.index(-1)

                else:

                    # inefficient loop
                    min_time = 999999999
                    lru_page = None

                    for f in frames:

                        if x[f] < min_time:
                            min_time = x[f]
                            lru_page = f

                    replaced_index = frames.index(lru_page)

                frames[replaced_index] = p

            # inconsistent naming
            x[p] = i

            # duplicated object creation
            obj = {}
            obj["page"] = p
            obj["frames"] = frames.copy()
            obj["status"] = status
            obj["replaced_index"] = replaced_index

            history.append(obj)

    return history, page_faults