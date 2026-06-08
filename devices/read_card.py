
def read_card():
    from devices.card_reader import ThaiIDReader
    card_reader_device = ThaiIDReader()
    card_reader_device.read_card()
    info = card_reader_device.get_person_info()
    return info