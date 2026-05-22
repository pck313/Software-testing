from algorithm import lru_page_replacement

def test_functional_basic_lru():
    pages = [1, 2, 3, 1, 4, 5]
    capacity = 3

    history, faults = lru_page_replacement(pages, capacity)

    assert len(history) == len(pages)
    assert faults > 0
    
def test_functional_repeated_access():
    pages = [1, 1, 1, 1]
    capacity = 2

    history, faults = lru_page_replacement(pages, capacity)

    assert faults >= 1
    assert history[-1]["page"] == 1
    
def test_functional_random_sequence():
    pages = [3, 2, 1, 4, 2, 5]
    capacity = 3

    history, faults = lru_page_replacement(pages, capacity)

    assert isinstance(history, list)
    assert isinstance(faults, int)
    
def test_control_flow_hit_case():
    pages = [1, 2, 1]
    capacity = 2

    history, _ = lru_page_replacement(pages, capacity)

    assert history[1]["status"] == "Ko lỗi"
    assert history[1]["replaced_index"] == -1
    
def test_control_flow_empty_slot():
    pages = [1, 2]
    capacity = 3

    history, _ = lru_page_replacement(pages, capacity)

    # chưa full nên không replace LRU
    assert -1 in history[1]["frames"]
    
def test_control_flow_replacement():
    pages = [1, 2, 3, 4]
    capacity = 3

    history, _ = lru_page_replacement(pages, capacity)

    assert any(h["replaced_index"] != -1 for h in history)

def test_control_flow_full_cycle():
    pages = [1, 2, 3, 1, 4]
    capacity = 3

    history, _ = lru_page_replacement(pages, capacity)

    assert history[-1]["frames"] is not None
    
def test_data_flow_history_changes():
    pages = [1, 2, 3]
    capacity = 2

    history, _ = lru_page_replacement(pages, capacity)

    assert history[0]["frames"] != history[-1]["frames"]
    
def test_data_flow_page_tracking():
    pages = [1, 2, 1]
    capacity = 2

    history, _ = lru_page_replacement(pages, capacity)

    assert history[-1]["page"] == 1

def test_data_flow_no_mutation_bug():
    pages = [1, 2, 3]
    capacity = 2

    history, _ = lru_page_replacement(pages, capacity)

    # kiểm history không bị overwrite toàn bộ
    assert len(set(id(h["frames"]) for h in history)) > 1

def test_mutation_fault_count():
    pages = [1, 2, 3]
    capacity = 2

    _, faults = lru_page_replacement(pages, capacity)

    assert faults >= 0
    
def test_mutation_replacement_occurs():
    pages = [1, 2, 3, 4]
    capacity = 3

    history, _ = lru_page_replacement(pages, capacity)

    assert any(h["replaced_index"] != -1 for h in history)
    
def test_mutation_hit_behavior():
    pages = [1, 2, 1]
    capacity = 2

    history, _ = lru_page_replacement(pages, capacity)

    assert history[2]["status"] == "Ko lỗi"
    
def test_empty_input():
    history, faults = lru_page_replacement([], 3)

    assert history == []
    assert faults == 0
    
def test_single_frame():
    pages = [1, 2, 3, 1]
    capacity = 1

    history, faults = lru_page_replacement(pages, capacity)

    assert len(history) == 4
    
def test_zero_capacity():
    pages = [1, 2, 3]

    history, faults = lru_page_replacement(pages, 0)

    assert history == []
    assert faults == 0
    