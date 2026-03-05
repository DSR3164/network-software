
# Реализуйте здесь простую машину состояний (State Machine).
# Функция должна принимать текущее состояние и событие,
# и возвращать следующее состояние.

def next_state(state: str, event: str) -> str:
    transitions = {
        ("NEW", "PAY_OK"): "PAID",
        ("NEW", "PAY_FAIL"): "CANCELLED",

        ("PAID", "PAID_OK"): "DONE",
        ("PAID", "PAID_FAIL"): "CANCELLED",

        ("DONE", "RESET"): "DONE",
        ("CANCELLED", "RETRY"): "CANCELLED",
    }

    return transitions.get((state, event), state)
