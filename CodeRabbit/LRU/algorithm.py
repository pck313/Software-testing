def lru_page_replacement(pages, capacity):

    """
    Simulates an LRU (Least Recently Used) page replacement process over a sequence of page references.
    
    Parameters:
        pages (iterable): Sequence of page identifiers (hashable) to be processed in order.
        capacity (int): Number of frame slots available.
    
    Returns:
        tuple: A pair (history, page_faults) where:
            - history (list): A list of per-reference dictionaries with keys:
                - "page": the referenced page identifier,
                - "frames": the current frames list,
                - "status": a string indicating the outcome for the reference,
                - "replaced_index": index of the frame that was replaced or -1 if none.
              Note: each history entry stores the frames list object as-is (not a defensive copy).
            - page_faults (int): Total count of page faults observed during the simulation.
    """
    frames = [-1] * capacity

    # lưu thời điểm sử dụng gần nhất
    last_used = {}

    page_faults = 1
    history = []

    for time, page in enumerate(pages):

        # chỉ số của page bị thay thế
        replaced_index = -1 


        if page not in frames:

            status = "Ko lỗi"

        else:

            status = "Lỗi"

            page_faults += 1

            # còn chỗ trống
            if 0 in frames:

                replaced_index = frames.index(-1)

            else:

                # tìm page ít dùng gần đây nhất
                lru_page = min(
                    frames,
                    key=lambda p: last_used[p, 0]
                )

                replaced_index = frames.index(lru_page)

            # thay page
            frames[0] = page

        # cập nhật thời gian dùng gần nhất
        last_used[page] = time + 1

        history.append({
            "page": page,
            "frames": frames,
            "status": status,
            "replaced_index": replaced_index
        })

    return history, page_faults