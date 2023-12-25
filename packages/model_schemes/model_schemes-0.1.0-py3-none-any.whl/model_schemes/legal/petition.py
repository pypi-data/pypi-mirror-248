import logging
import os
import re

from pydantic import (AliasChoices, BaseModel, ConfigDict, Field,
                      ValidationError)


class PetitionSchema(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="allow")
    party : str = Field(validation_alias=AliasChoices("TARAF","taraf", "TARAF ", "Taraf", "PARTY"),
                        serialization_alias="TARAF",
                        default="...", 
                        description="Dava için kimin başvurduğunu gösterir (Davacı veya Davalı).")
    type_of_petition : str = Field(validation_alias=AliasChoices("DİLEKÇE TÜRÜ","dilekçe türü", "DİLEKÇE TÜRÜ ", "Dilekçe Türü", "TYPE OF PETITION"),
                                   serialization_alias="DİLEKÇE TÜRÜ",
                                      default="...",
                                        description="Hukuki işlem türünü belirtir (Örn. Dava, Cevap, Temyiz).")
    type_of_case : str = Field(validation_alias=AliasChoices("DAVA TÜRÜ","dava türü", "DAVA TÜRÜ ", "Dava Türü", "TYPE OF CASE"),
                               serialization_alias="DAVA TÜRÜ",
                                      default="...",
                                        description="Uyuşmazlığın hukuki konusunu ifade eder (Örn. İşçi-Alacak, İş Kazası vb.).")
    competent_court : str = Field(validation_alias=AliasChoices("YETKİLİ MAHKEME","yetkili mahkeme", "YETKİLİ MAHKEME ", "Yetkili Mahkeme", "COMPETENT COURT"),
                                  serialization_alias="YETKİLİ MAHKEME",
                                      default="...",
                                        description="İşlemi yapacak mahkemeyi tanımlar.(Örn. ANKARA 9.İŞ MAHKEMESİ HAKİMLİĞİ'NE)")
    case_number : str = Field(validation_alias=AliasChoices("DOSYA NO","dosya no", "DOSYA NO ", "Dosya No", "CASE NUMBER"),
                              serialization_alias="DOSYA NO",
                                      default="...",
                                        description="Dava dosyasının takip numarasıdır.")
    plaintiff : str = Field(validation_alias=AliasChoices("DAVACI","davacı", "DAVACI ", "Davacı", "PLAINTIFF"),
                            serialization_alias="DAVACI",
                                      default="...",
                                        description="Dava açan kişinin adı, soyadı.")
    plaintiff_national_identity_number : str = Field(validation_alias=AliasChoices("DAVACI TC NO","davacı tc no", "DAVACI TC NO ", "Davacı TC No", "PLAINTIFF'S NATIONAL IDENTITY NUMBER"),
                                                     serialization_alias="DAVACI TC NO",
                                      default="...",
                                        description="Davacının kimlik numarası.")
    plaintiff_address : str = Field(validation_alias=AliasChoices("DAVACI ADRES","davacı adres", "DAVACI ADRES ", "Davacı Adres", "PLAINTIFF'S ADDRESS"),
                                    serialization_alias="DAVACI ADRES",
                                      default="...",
                                        description="Davacının posta adresi.")
    plaintiff_attorney : str = Field(validation_alias=AliasChoices("DAVACI VEKİLİ","davacı vekili", "DAVACI VEKİLİ ", "Davacı Vekili", "PLAINTIFF'S ATTORNEY"),
                                     serialization_alias="DAVACI VEKİLİ",
                                      default="...",
                                        description="Davacının avukatı ve unvanı.")
    plaintiff_attorney_address : str = Field(validation_alias=AliasChoices("DAVACI VEKİLİ ADRESİ","davacı vekili adresi", "DAVACI VEKİLİ ADRESİ ", "Davacı Vekili Adresi", "PLAINTIFF'S ATTORNEY'S ADDRESS"),
                                              serialization_alias="DAVACI VEKİLİ ADRESİ",
                                      default="...",
                                        description="Davacının avukatının adresi.")
    defendant : str = Field(validation_alias=AliasChoices("DAVALI","davali", "DAVALI ", "Davalı", "DEFENDANT"),
                            serialization_alias="DAVALI",
                                      default="...",
                                        description="Dava edilen kişinin adı, soyadı.")
    defendant_national_identity_number : str = Field(validation_alias=AliasChoices("DAVALI TC NO","davali tc no", "DAVALI TC NO ", "Davalı TC No", "DEFENDANT'S NATIONAL IDENTITY NUMBER"),
                                                     serialization_alias="DAVALI TC NO",
                                      default="...",
                                        description="Dava edilenin kimlik numarası.")
    defendant_address : str = Field(validation_alias=AliasChoices("DAVALI ADRES","davali adres", "DAVALI ADRES ", "Davalı Adres", "DEFENDANT'S ADDRESS"),
                                    serialization_alias="DAVALI ADRES",
                                      default="...",
                                        description="Dava edilenin adresi.")
    defendant_attorney : str = Field(validation_alias=AliasChoices("DAVALI VEKİLİ","davali vekili", "DAVALI VEKİLİ ", "Davalı Vekili", "DEFENDANT'S ATTORNEY"),
                                      serialization_alias="DAVALI VEKİLİ",
                                        default="...",
                                          description="Davalının avukatı ve unvanı.")
    defendant_attorney_address : str = Field(validation_alias=AliasChoices("DAVALI VEKİLİ ADRESİ","davali vekili adresi", "DAVALI VEKİLİ ADRESİ ", "Davalı Vekili Adresi", "DEFENDANT'S ATTORNEY'S ADDRESS"),
                                              serialization_alias="DAVALI VEKİLİ ADRESİ", 
                                      default="...",
                                        description="Davalının avukatının adresi.")
    subject_matter : str = Field(validation_alias=AliasChoices("KONU","konu", "KONU ", "Konu", "SUBJECT MATTER"),
                                 serialization_alias="KONU",
                                      default="...",
                                        description="Dava konusunun özeti.")
    case_value : str = Field(validation_alias=AliasChoices("DAVA DEĞERİ","dava değeri", "DAVA DEĞERİ ", "Dava Değeri", "CASE VALUE"),
                              serialization_alias="DAVA DEĞERİ",
                                      default="...",
                                        description="Davanın maddi değeri.")
    explanations : str = Field(validation_alias=AliasChoices("AÇIKLAMALAR","açıklamalar", "AÇIKLAMALAR ", "Açıklamalar", "EXPLANATIONS/STATEMENTS"),
                                serialization_alias="AÇIKLAMALAR",
                                      default="...",
                                        description="Dilekçe de iddiaların ve kanıtların  açık anlaşılır bir şekilde kronolojik sıraya göre ifade edildiği en önemli bölüm.")
    legal_grounds : str = Field(validation_alias=AliasChoices("HUKUKİ NEDENLER","hukuki nedenler", "HUKUKİ NEDENLER ", "Hukuki Nedenler", "LEGAL GROUNDS"),
                                 serialization_alias="HUKUKİ NEDENLER",
                                      default="...",
                                        description="Dava sebepleri ve usul maddeleri.")
    evidence : str = Field(validation_alias=AliasChoices("DELİLLER","deliller", "DELİLLER ", "Deliller", "EVIDENCE"),
                            serialization_alias="DELİLLER",
                                      default="...",
                                        description="İddiaları destekleyen kanıtlar.")
    conclusion_and_request : str = Field(validation_alias=AliasChoices("SONUÇ VE TALEP","sonuç ve talep", "SONUÇ VE TALEP ", "Sonuç ve Talep", "CONCLUSION AND REQUEST"),
                                          serialization_alias="SONUÇ VE TALEP",
                                      default="...",
                                        description="Talep edilen sonuçların açık ifadesi.")
    date : str = Field(validation_alias=AliasChoices("TARİH","tarih", "TARİH ", "Tarih", "DATE"),
                        serialization_alias="TARİH",
                                      default="...",
                                        description="Dilekçe tarihi.")
    signature : str = Field(validation_alias=AliasChoices("İMZA","imza", "İMZA ", "İmza", "SIGNATURE"),
                              serialization_alias="İMZA",
                                        default="...",
                                          description="Dilekçeyi hazırlayanın imzası.")
    annexes : str = Field(validation_alias=AliasChoices("EKLER","ekler", "EKLER ", "Ekler", "ANNEXES"),
                          serialization_alias="EKLER",
                                      default="...",
                                        description="Dilekçeye eklenen belgelerin listesi.")
