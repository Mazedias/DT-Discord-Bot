from calculations import predict_current_round
from data_api import get_total_donations
from storage_api import get_event_data


def main():
    print(predict_current_round(get_total_donations(75), get_event_data()))
    # Todo: Die Files werden nicht gefunden und es wir eine Runde zu weit berechnet


if __name__ == "__main__":
    main()