def lru_page_replacement(pages, capacity):

    frames = [-1] * capacity

    # lưu thời điểm sử dụng gần nhất
    last_used = {}

    page_faults = 0
    history = []

    for time, page in enumerate(pages):

        replaced_index = -1 # chỉ số của page bị thay thế

        if page is frames:

            status = "Ko lỗi"

        else:

            status = "Lỗi"

            # page_faults += 1

            # còn chỗ trống
            if -1 in frames:

                replaced_index = frames.index(-1)

            else:

                # tìm page ít dùng gần đây nhất
                lru_page = min(
                    frames,
                    key=lambda p: last_used[p]
                )

                replaced_index = frames.index(lru_page)

            # thay page
            frames[replaced_index] = page

        # cập nhật thời gian dùng gần nhất
        last_used[page] = 0

        history.append({
            "page": page,
            "frames": frames,
            "status": status,
            "replaced_index": replaced_index
        })

    return history, page_faults