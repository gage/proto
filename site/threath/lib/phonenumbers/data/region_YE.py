"""Auto-generated file, do not edit by hand. YE metadata"""
from phonenumbers import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_YE = PhoneMetadata(id='YE', country_code=967, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern=u'[1-7]\d{6,8}', possible_number_pattern=u'\d{6,9}'),
    fixed_line=PhoneNumberDesc(national_number_pattern=u'(?:1(?:7\d|[2-68])|2[2-68]|3[2358]|4[2-58]|5[2-6]|6[3-58]|7[24-68])\d{5}', possible_number_pattern=u'\d{6,8}', example_number=u'1234567'),
    mobile=PhoneNumberDesc(national_number_pattern=u'7[137]\d{7}', possible_number_pattern=u'\d{9}', example_number=u'712345678'),
    toll_free=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    premium_rate=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    shared_cost=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    personal_number=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    voip=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    pager=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    uan=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    no_international_dialling=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    national_prefix=u'0',
    national_prefix_for_parsing=u'0',
    number_format=[NumberFormat(pattern='([1-7])(\d{3})(\d{3,4})', format=u'\\1 \\2 \\3', leading_digits_pattern=['[1-6]|7[24-68]'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(7[137]\d)(\d{3})(\d{3})', format=u'\\1 \\2 \\3', leading_digits_pattern=['7[137]'], national_prefix_formatting_rule=u'0\\1')])
