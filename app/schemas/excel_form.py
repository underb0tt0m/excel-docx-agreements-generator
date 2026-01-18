from pydantic import BaseModel, ConfigDict, Field, model_validator, ValidationError

class AgreementExcelModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    needs_brd: str = Field(
        ...,
        validation_alias="Needs_brd",
        serialization_alias="Needs_brd"
    )
    needs_edo: str = Field(
        ...,
        validation_alias="Needs_EDO",
        serialization_alias="Needs_EDO"
    )
    ka_type: str = Field(
        ...,
        validation_alias="KA_type",
        serialization_alias="KA_type"
    )

    name_full: str = Field(
        ...,
        validation_alias="Full_organization_2_name",
        serialization_alias="Full_organization_2_name")
    name_short: str = Field(
        ...,
        validation_alias="Abbreviated_organization_2_name",
        serialization_alias="Abbreviated_organization_2_name")

    pos_org_2_rep_nom: str = Field(
        ...,
        validation_alias="The_position_of_the_organization_2_representative_in_the_nominative_case",
        serialization_alias="The_position_of_the_organization_2_representative_in_the_nominative_case"
    )
    pos_org_2_rep_gen: str = Field(
        ...,
        validation_alias="The_position_of_the_organization_2_representative_in_the_genitive_case",
        serialization_alias="The_position_of_the_organization_2_representative_in_the_genitive_case"
    )
    name_full_org_2_rep_nom: str = Field(
        ...,
        validation_alias="Full_name_of_the_organization_2_representative_in_the_nominative_case",
        serialization_alias="Full_name_of_the_organization_2_representative_in_the_nominative_case"
    )
    name_full_org_2_rep_gen: str = Field(
        ...,
        validation_alias="Full_name_of_the_organization_2_representative_in_the_genitive_case",
        serialization_alias="Full_name_of_the_organization_2_representative_in_the_genitive_case"
    )
    auth_org_2_rep: str = Field(
        ...,
        validation_alias="The_authority_of_the_organization_2_representative",
        serialization_alias="The_authority_of_the_organization_2_representative")
    edo_op: str = Field(
        ...,
        validation_alias="EDO_operator",
        serialization_alias="EDO_operator"
    )
    mail: str = Field(
        ...,
        validation_alias="Mail",
        serialization_alias="Mail"
    )
    ogrn: str | int = Field(
        ...,
        validation_alias="OGRN",
        serialization_alias="OGRN"
    )
    inn: str | int = Field(
        ...,
        validation_alias="INN",
        serialization_alias="INN"
    )
    kpp: str | int = Field(
        ...,
        validation_alias="KPP",
        serialization_alias="KPP"
    )
    okpo: str | int = Field(
        ...,
        validation_alias="OKPO",
        serialization_alias="OKPO"
    )
    okved: str = Field(
        ...,
        validation_alias="OKVED",
        serialization_alias="OKVED"
    )
    okato: str | int = Field(
        ...,
        validation_alias="OKATO",
        serialization_alias="OKATO"
    )
    jur_address: str = Field(
        ...,
        validation_alias="Juridical_address",
        serialization_alias="Juridical_address"
    )
    phys_address: str = Field(
        ...,
        validation_alias="Physical_address",
        serialization_alias="Physical_address"
    )
    sw_name: str | None = Field(
        None,
        validation_alias="SW_name",
        serialization_alias="SW_name"
    )
    sw_registration: str | None = Field(
        None,
        validation_alias="SW_registration",
        serialization_alias="SW_registration"
    )
    sw_reg_number: str | None = Field(
        None,
        validation_alias="Register_number",
        serialization_alias="Register_number"
    )
    copyright_holder_url: str | None = Field(
        None,
        validation_alias="Copyright_holder_url",
        serialization_alias="Copyright_holder_url"
    )
    is_copyright_holder_url_or_not: str | None = Field(
        None,
        validation_alias="Is_copyright_holder_url_or_not",
        serialization_alias="Is_copyright_holder_url_or_not"
    )
    web_owner: str | None = Field(
        None,
        validation_alias="Web_owner",
        serialization_alias="Web_owner"
    )

    @model_validator(mode="after")
    def check_service_fields(self):
        if self.ka_type == "Услуга":
            return self

        required = {
            "sw_name": "Название программы ЭВМ",
            "sw_registration": "Свидетельство о государственной регистрации программы ЭВМ",
            "sw_reg_number": "Реестровая запись в реестре РПО",
            "copyright_holder_url": "Сайт с условиями предоставления",
            "is_copyright_holder_url_or_not": "Поставщик правообладатель?",
            "web_owner": "Поставщик администратор?",
        }

        errors = []

        for field_name, field_description in required.items():
            if getattr(self, field_name) is None:
                errors.append({
                    "type": "value_error",
                    "loc": (field_name,),
                    "msg": f"Для {self.name_short} не заполнено поле '{field_description}'",
                    "input": None,
                    "ctx": {"error": f"Поле '{field_description}' обязательно"}
                })

        if errors:
            raise ValidationError.from_exception_data(
                "Service fields validation failed",
                errors
            )

        return self
