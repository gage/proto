"""Auto-generated file, do not edit by hand. MA metadata"""
from phonenumbers import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_MA = PhoneMetadata(id='MA', country_code=212, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern=u'[5689]\d{8}', possible_number_pattern=u'\d{9}'),
    fixed_line=PhoneNumberDesc(national_number_pattern=u'5(?:2(?:(?:[015-7]\d|2[2-9]|3[2-57]|4[2-8]|8[235-9]|)\d|9(?:0\d|[89]0))|3(?:(?:[0-4]\d|[57][2-9]|6[235-8]|9[3-9])\d|8(?:0\d|[89]0)))\d{4}', possible_number_pattern=u'\d{9}', example_number=u'520123456'),
    mobile=PhoneNumberDesc(national_number_pattern=u'6(?:0[06]|[14-7]\d|2[236]|33|99)\d{6}', possible_number_pattern=u'\d{9}', example_number=u'650123456'),
    toll_free=PhoneNumberDesc(national_number_pattern=u'80\d{7}', possible_number_pattern=u'\d{9}', example_number=u'801234567'),
    premium_rate=PhoneNumberDesc(national_number_pattern=u'89\d{7}', possible_number_pattern=u'\d{9}', example_number=u'891234567'),
    shared_cost=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    personal_number=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    voip=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    pager=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    uan=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    no_international_dialling=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    national_prefix=u'0',
    national_prefix_for_parsing=u'0',
    number_format=[NumberFormat(pattern='([56]\d{2})(\d{6})', format=u'\\1-\\2', leading_digits_pattern=['5(?:2[015-7]|3[0-4])|6'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='([58]\d{3})(\d{5})', format=u'\\1-\\2', leading_digits_pattern=['5(?:2[2-489]|3[5-9])|892', '5(?:2(?:[2-48]|90)|3(?:[5-79]|80))|892'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(5\d{4})(\d{4})', format=u'\\1-\\2', leading_digits_pattern=['5(?:29|38)', '5(?:29|38)[89]'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(8[09])(\d{7})', format=u'\\1-\\2', leading_digits_pattern=['8(?:0|9[013-9])'], national_prefix_formatting_rule=u'0\\1')])
