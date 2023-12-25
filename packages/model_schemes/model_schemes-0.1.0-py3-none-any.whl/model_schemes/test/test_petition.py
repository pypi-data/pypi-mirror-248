from pydantic import (AliasChoices, BaseModel, ConfigDict, Field,
                      ValidationError)

# sample_data = {
#     "TARAF": "Davacı",
#     "DİLEKÇE TÜRÜ": "Dava",
#     "DAVA TÜRÜ": "İşçi-Alacak",
#     "YETKİLİ MAHKEME": "ANKARA 9.İŞ MAHKEMESİ HAKİMLİĞİ'NE",
#     "DOSYA NO": "2021/123",
#     "DAVACI": "Ali Veli",
#     "DAVACI TC NO": "12345678901",
#     "DAVACI ADRES": "Ankara",
#     "DAVACI VEKİLİ": "Av. Ahmet Mehmet",
#     "DAVACI VEKİLİ ADRESİ": "Ankara",
#     "DAVALI": "Ayşe Fatma",
#     "DAVALI TC NO": "12345678901",
#     "DAVALI ADRES": "Ankara",
#     "DAVALI VEKİLİ": "Av. Mehmet Ahmet",
#     "DAVALI VEKİLİ ADRESİ": "Ankara",
#     "KONU": "İşçi Alacakları",
#     "DAVA DEĞERİ": "10000",
#     "AÇIKLAMALAR": "İşçi Ali Veli işveren Ayşe Fatma'ya ait şirkette çalışmaktadır...",
#     "HUKUKİ NEDENLER": "İş Kanunu, Borçlar Kanunu",
#     "DELİLLER": "İşçi Alacakları",
#     "SONUÇ VE TALEP": "İşçi Alacaklarını talep ederim.",
#     "TARİH": "01.01.2021",
#     "EKLER": "1. İş Sözleşmesi\n2. İş Kanunu",
#     "İMZA": "Av. Ahmet Mehmet"
# }
    
# # write a pytest for testing PetitionSchema
# try:
#     p = PetitionSchema(**sample_data)
# except ValidationError as e:
#     print(e)



# if __name__ == "__main__":
#     petition = PetitionSchema(**sample_data)
#     print(petition.model_dump_json(indent=2))