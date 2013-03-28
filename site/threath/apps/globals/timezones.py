import datetime
import pytz

from django.utils.translation import ugettext_lazy as _

TIMEZONE_TRANSLATION = {
    'Pacific/Apia': _('Pacific/Apia'),
    'Pacific/Midway': _('Pacific/Midway'),
    'Pacific/Niue': _('Pacific/Niue'),
    'Pacific/Pago_Pago': _('Pacific/Pago_Pago'),
    'America/Adak': _('America/Adak'),
    'Pacific/Fakaofo': _('Pacific/Fakaofo'),
    'Pacific/Honolulu': _('Pacific/Honolulu'),
    'Pacific/Johnston': _('Pacific/Johnston'),
    'Pacific/Rarotonga': _('Pacific/Rarotonga'),
    'Pacific/Tahiti': _('Pacific/Tahiti'),
    'US/Hawaii': _('US/Hawaii'),
    'Pacific/Marquesas': _('Pacific/Marquesas'),
    'America/Anchorage': _('America/Anchorage'),
    'America/Juneau': _('America/Juneau'),
    'America/Nome': _('America/Nome'),
    'America/Sitka': _('America/Sitka'),
    'America/Yakutat': _('America/Yakutat'),
    'Pacific/Gambier': _('Pacific/Gambier'),
    'US/Alaska': _('US/Alaska'),
    'America/Dawson': _('America/Dawson'),
    'America/Los_Angeles': _('America/Los_Angeles'),
    'America/Metlakatla': _('America/Metlakatla'),
    'America/Santa_Isabel': _('America/Santa_Isabel'),
    'America/Tijuana': _('America/Tijuana'),
    'America/Vancouver': _('America/Vancouver'),
    'America/Whitehorse': _('America/Whitehorse'),
    'Canada/Pacific': _('Canada/Pacific'),
    'Pacific/Pitcairn': _('Pacific/Pitcairn'),
    'US/Pacific': _('US/Pacific'),
    'America/Boise': _('America/Boise'),
    'America/Cambridge_Bay': _('America/Cambridge_Bay'),
    'America/Chihuahua': _('America/Chihuahua'),
    'America/Dawson_Creek': _('America/Dawson_Creek'),
    'America/Denver': _('America/Denver'),
    'America/Edmonton': _('America/Edmonton'),
    'America/Hermosillo': _('America/Hermosillo'),
    'America/Inuvik': _('America/Inuvik'),
    'America/Mazatlan': _('America/Mazatlan'),
    'America/Ojinaga': _('America/Ojinaga'),
    'America/Phoenix': _('America/Phoenix'),
    'America/Shiprock': _('America/Shiprock'),
    'America/Yellowknife': _('America/Yellowknife'),
    'Canada/Mountain': _('Canada/Mountain'),
    'US/Arizona': _('US/Arizona'),
    'US/Mountain': _('US/Mountain'),
    'America/Bahia_Banderas': _('America/Bahia_Banderas'),
    'America/Belize': _('America/Belize'),
    'America/Cancun': _('America/Cancun'),
    'America/Chicago': _('America/Chicago'),
    'America/Costa_Rica': _('America/Costa_Rica'),
    'America/El_Salvador': _('America/El_Salvador'),
    'America/Guatemala': _('America/Guatemala'),
    'America/Indiana/Knox': _('America/Indiana/Knox'),
    'America/Indiana/Tell_City': _('America/Indiana/Tell_City'),
    'America/Managua': _('America/Managua'),
    'America/Matamoros': _('America/Matamoros'),
    'America/Menominee': _('America/Menominee'),
    'America/Merida': _('America/Merida'),
    'America/Mexico_City': _('America/Mexico_City'),
    'America/Monterrey': _('America/Monterrey'),
    'America/North_Dakota/Beulah': _('America/North_Dakota/Beulah'),
    'America/North_Dakota/Center': _('America/North_Dakota/Center'),
    'America/North_Dakota/New_Salem': _('America/North_Dakota/New_Salem'),
    'America/Rainy_River': _('America/Rainy_River'),
    'America/Rankin_Inlet': _('America/Rankin_Inlet'),
    'America/Regina': _('America/Regina'),
    'America/Swift_Current': _('America/Swift_Current'),
    'America/Tegucigalpa': _('America/Tegucigalpa'),
    'America/Winnipeg': _('America/Winnipeg'),
    'Canada/Central': _('Canada/Central'),
    'Pacific/Galapagos': _('Pacific/Galapagos'),
    'US/Central': _('US/Central'),
    'America/Atikokan': _('America/Atikokan'),
    'America/Bogota': _('America/Bogota'),
    'America/Cayman': _('America/Cayman'),
    'America/Detroit': _('America/Detroit'),
    'America/Grand_Turk': _('America/Grand_Turk'),
    'America/Guayaquil': _('America/Guayaquil'),
    'America/Havana': _('America/Havana'),
    'America/Indiana/Indianapolis': _('America/Indiana/Indianapolis'),
    'America/Indiana/Marengo': _('America/Indiana/Marengo'),
    'America/Indiana/Petersburg': _('America/Indiana/Petersburg'),
    'America/Indiana/Vevay': _('America/Indiana/Vevay'),
    'America/Indiana/Vincennes': _('America/Indiana/Vincennes'),
    'America/Indiana/Winamac': _('America/Indiana/Winamac'),
    'America/Iqaluit': _('America/Iqaluit'),
    'America/Jamaica': _('America/Jamaica'),
    'America/Kentucky/Louisville': _('America/Kentucky/Louisville'),
    'America/Kentucky/Monticello': _('America/Kentucky/Monticello'),
    'America/Lima': _('America/Lima'),
    'America/Montreal': _('America/Montreal'),
    'America/Nassau': _('America/Nassau'),
    'America/New_York': _('America/New_York'),
    'America/Nipigon': _('America/Nipigon'),
    'America/Panama': _('America/Panama'),
    'America/Pangnirtung': _('America/Pangnirtung'),
    'America/Port-au-Prince': _('America/Port-au-Prince'),
    'America/Resolute': _('America/Resolute'),
    'America/Thunder_Bay': _('America/Thunder_Bay'),
    'America/Toronto': _('America/Toronto'),
    'Canada/Eastern': _('Canada/Eastern'),
    'Pacific/Easter': _('Pacific/Easter'),
    'US/Eastern': _('US/Eastern'),
    'America/Caracas': _('America/Caracas'),
    'America/Anguilla': _('America/Anguilla'),
    'America/Antigua': _('America/Antigua'),
    'America/Aruba': _('America/Aruba'),
    'America/Barbados': _('America/Barbados'),
    'America/Blanc-Sablon': _('America/Blanc-Sablon'),
    'America/Boa_Vista': _('America/Boa_Vista'),
    'America/Curacao': _('America/Curacao'),
    'America/Dominica': _('America/Dominica'),
    'America/Eirunepe': _('America/Eirunepe'),
    'America/Glace_Bay': _('America/Glace_Bay'),
    'America/Goose_Bay': _('America/Goose_Bay'),
    'America/Grenada': _('America/Grenada'),
    'America/Guadeloupe': _('America/Guadeloupe'),
    'America/Guyana': _('America/Guyana'),
    'America/Halifax': _('America/Halifax'),
    'America/Kralendijk': _('America/Kralendijk'),
    'America/La_Paz': _('America/La_Paz'),
    'America/Lower_Princes': _('America/Lower_Princes'),
    'America/Manaus': _('America/Manaus'),
    'America/Marigot': _('America/Marigot'),
    'America/Martinique': _('America/Martinique'),
    'America/Moncton': _('America/Moncton'),
    'America/Montserrat': _('America/Montserrat'),
    'America/Port_of_Spain': _('America/Port_of_Spain'),
    'America/Porto_Velho': _('America/Porto_Velho'),
    'America/Puerto_Rico': _('America/Puerto_Rico'),
    'America/Rio_Branco': _('America/Rio_Branco'),
    'America/Santo_Domingo': _('America/Santo_Domingo'),
    'America/St_Barthelemy': _('America/St_Barthelemy'),
    'America/St_Kitts': _('America/St_Kitts'),
    'America/St_Lucia': _('America/St_Lucia'),
    'America/St_Thomas': _('America/St_Thomas'),
    'America/St_Vincent': _('America/St_Vincent'),
    'America/Thule': _('America/Thule'),
    'America/Tortola': _('America/Tortola'),
    'Atlantic/Bermuda': _('Atlantic/Bermuda'),
    'Canada/Atlantic': _('Canada/Atlantic'),
    'America/St_Johns': _('America/St_Johns'),
    'Canada/Newfoundland': _('Canada/Newfoundland'),
    'America/Araguaina': _('America/Araguaina'),
    'America/Argentina/Buenos_Aires': _('America/Argentina/Buenos_Aires'),
    'America/Argentina/Catamarca': _('America/Argentina/Catamarca'),
    'America/Argentina/Cordoba': _('America/Argentina/Cordoba'),
    'America/Argentina/Jujuy': _('America/Argentina/Jujuy'),
    'America/Argentina/La_Rioja': _('America/Argentina/La_Rioja'),
    'America/Argentina/Mendoza': _('America/Argentina/Mendoza'),
    'America/Argentina/Rio_Gallegos': _('America/Argentina/Rio_Gallegos'),
    'America/Argentina/Salta': _('America/Argentina/Salta'),
    'America/Argentina/San_Juan': _('America/Argentina/San_Juan'),
    'America/Argentina/San_Luis': _('America/Argentina/San_Luis'),
    'America/Argentina/Tucuman': _('America/Argentina/Tucuman'),
    'America/Argentina/Ushuaia': _('America/Argentina/Ushuaia'),
    'America/Asuncion': _('America/Asuncion'),
    'America/Bahia': _('America/Bahia'),
    'America/Belem': _('America/Belem'),
    'America/Campo_Grande': _('America/Campo_Grande'),
    'America/Cayenne': _('America/Cayenne'),
    'America/Cuiaba': _('America/Cuiaba'),
    'America/Fortaleza': _('America/Fortaleza'),
    'America/Godthab': _('America/Godthab'),
    'America/Maceio': _('America/Maceio'),
    'America/Miquelon': _('America/Miquelon'),
    'America/Paramaribo': _('America/Paramaribo'),
    'America/Recife': _('America/Recife'),
    'America/Santarem': _('America/Santarem'),
    'America/Santiago': _('America/Santiago'),
    'Antarctica/Palmer': _('Antarctica/Palmer'),
    'Antarctica/Rothera': _('Antarctica/Rothera'),
    'Atlantic/Stanley': _('Atlantic/Stanley'),
    'America/Montevideo': _('America/Montevideo'),
    'America/Noronha': _('America/Noronha'),
    'America/Sao_Paulo': _('America/Sao_Paulo'),
    'Atlantic/South_Georgia': _('Atlantic/South_Georgia'),
    'America/Scoresbysund': _('America/Scoresbysund'),
    'Atlantic/Azores': _('Atlantic/Azores'),
    'Atlantic/Cape_Verde': _('Atlantic/Cape_Verde'),
    'Africa/Abidjan': _('Africa/Abidjan'),
    'Africa/Accra': _('Africa/Accra'),
    'Africa/Bamako': _('Africa/Bamako'),
    'Africa/Banjul': _('Africa/Banjul'),
    'Africa/Bissau': _('Africa/Bissau'),
    'Africa/Casablanca': _('Africa/Casablanca'),
    'Africa/Conakry': _('Africa/Conakry'),
    'Africa/Dakar': _('Africa/Dakar'),
    'Africa/El_Aaiun': _('Africa/El_Aaiun'),
    'Africa/Freetown': _('Africa/Freetown'),
    'Africa/Lome': _('Africa/Lome'),
    'Africa/Monrovia': _('Africa/Monrovia'),
    'Africa/Nouakchott': _('Africa/Nouakchott'),
    'Africa/Ouagadougou': _('Africa/Ouagadougou'),
    'Africa/Sao_Tome': _('Africa/Sao_Tome'),
    'America/Danmarkshavn': _('America/Danmarkshavn'),
    'Atlantic/Canary': _('Atlantic/Canary'),
    'Atlantic/Faroe': _('Atlantic/Faroe'),
    'Atlantic/Madeira': _('Atlantic/Madeira'),
    'Atlantic/Reykjavik': _('Atlantic/Reykjavik'),
    'Atlantic/St_Helena': _('Atlantic/St_Helena'),
    'Europe/Dublin': _('Europe/Dublin'),
    'Europe/Guernsey': _('Europe/Guernsey'),
    'Europe/Isle_of_Man': _('Europe/Isle_of_Man'),
    'Europe/Jersey': _('Europe/Jersey'),
    'Europe/Lisbon': _('Europe/Lisbon'),
    'Europe/London': _('Europe/London'),
    'GMT': _('GMT'),
    'UTC': _('UTC'),
    'Africa/Algiers': _('Africa/Algiers'),
    'Africa/Bangui': _('Africa/Bangui'),
    'Africa/Brazzaville': _('Africa/Brazzaville'),
    'Africa/Ceuta': _('Africa/Ceuta'),
    'Africa/Douala': _('Africa/Douala'),
    'Africa/Kinshasa': _('Africa/Kinshasa'),
    'Africa/Lagos': _('Africa/Lagos'),
    'Africa/Libreville': _('Africa/Libreville'),
    'Africa/Luanda': _('Africa/Luanda'),
    'Africa/Malabo': _('Africa/Malabo'),
    'Africa/Ndjamena': _('Africa/Ndjamena'),
    'Africa/Niamey': _('Africa/Niamey'),
    'Africa/Porto-Novo': _('Africa/Porto-Novo'),
    'Africa/Tunis': _('Africa/Tunis'),
    'Arctic/Longyearbyen': _('Arctic/Longyearbyen'),
    'Europe/Amsterdam': _('Europe/Amsterdam'),
    'Europe/Andorra': _('Europe/Andorra'),
    'Europe/Belgrade': _('Europe/Belgrade'),
    'Europe/Berlin': _('Europe/Berlin'),
    'Europe/Bratislava': _('Europe/Bratislava'),
    'Europe/Brussels': _('Europe/Brussels'),
    'Europe/Budapest': _('Europe/Budapest'),
    'Europe/Copenhagen': _('Europe/Copenhagen'),
    'Europe/Gibraltar': _('Europe/Gibraltar'),
    'Europe/Ljubljana': _('Europe/Ljubljana'),
    'Europe/Luxembourg': _('Europe/Luxembourg'),
    'Europe/Madrid': _('Europe/Madrid'),
    'Europe/Malta': _('Europe/Malta'),
    'Europe/Monaco': _('Europe/Monaco'),
    'Europe/Oslo': _('Europe/Oslo'),
    'Europe/Paris': _('Europe/Paris'),
    'Europe/Podgorica': _('Europe/Podgorica'),
    'Europe/Prague': _('Europe/Prague'),
    'Europe/Rome': _('Europe/Rome'),
    'Europe/San_Marino': _('Europe/San_Marino'),
    'Europe/Sarajevo': _('Europe/Sarajevo'),
    'Europe/Skopje': _('Europe/Skopje'),
    'Europe/Stockholm': _('Europe/Stockholm'),
    'Europe/Tirane': _('Europe/Tirane'),
    'Europe/Vaduz': _('Europe/Vaduz'),
    'Europe/Vatican': _('Europe/Vatican'),
    'Europe/Vienna': _('Europe/Vienna'),
    'Europe/Warsaw': _('Europe/Warsaw'),
    'Europe/Zagreb': _('Europe/Zagreb'),
    'Europe/Zurich': _('Europe/Zurich'),
    'Africa/Blantyre': _('Africa/Blantyre'),
    'Africa/Bujumbura': _('Africa/Bujumbura'),
    'Africa/Cairo': _('Africa/Cairo'),
    'Africa/Gaborone': _('Africa/Gaborone'),
    'Africa/Harare': _('Africa/Harare'),
    'Africa/Johannesburg': _('Africa/Johannesburg'),
    'Africa/Juba': _('Africa/Juba'),
    'Africa/Kigali': _('Africa/Kigali'),
    'Africa/Lubumbashi': _('Africa/Lubumbashi'),
    'Africa/Lusaka': _('Africa/Lusaka'),
    'Africa/Maputo': _('Africa/Maputo'),
    'Africa/Maseru': _('Africa/Maseru'),
    'Africa/Mbabane': _('Africa/Mbabane'),
    'Africa/Tripoli': _('Africa/Tripoli'),
    'Africa/Windhoek': _('Africa/Windhoek'),
    'Asia/Amman': _('Asia/Amman'),
    'Asia/Beirut': _('Asia/Beirut'),
    'Asia/Damascus': _('Asia/Damascus'),
    'Asia/Gaza': _('Asia/Gaza'),
    'Asia/Jerusalem': _('Asia/Jerusalem'),
    'Asia/Nicosia': _('Asia/Nicosia'),
    'Europe/Athens': _('Europe/Athens'),
    'Europe/Bucharest': _('Europe/Bucharest'),
    'Europe/Chisinau': _('Europe/Chisinau'),
    'Europe/Helsinki': _('Europe/Helsinki'),
    'Europe/Istanbul': _('Europe/Istanbul'),
    'Europe/Kiev': _('Europe/Kiev'),
    'Europe/Mariehamn': _('Europe/Mariehamn'),
    'Europe/Minsk': _('Europe/Minsk'),
    'Europe/Riga': _('Europe/Riga'),
    'Europe/Simferopol': _('Europe/Simferopol'),
    'Europe/Sofia': _('Europe/Sofia'),
    'Europe/Tallinn': _('Europe/Tallinn'),
    'Europe/Uzhgorod': _('Europe/Uzhgorod'),
    'Europe/Vilnius': _('Europe/Vilnius'),
    'Europe/Zaporozhye': _('Europe/Zaporozhye'),
    'Africa/Addis_Ababa': _('Africa/Addis_Ababa'),
    'Africa/Asmara': _('Africa/Asmara'),
    'Africa/Dar_es_Salaam': _('Africa/Dar_es_Salaam'),
    'Africa/Djibouti': _('Africa/Djibouti'),
    'Africa/Kampala': _('Africa/Kampala'),
    'Africa/Khartoum': _('Africa/Khartoum'),
    'Africa/Mogadishu': _('Africa/Mogadishu'),
    'Africa/Nairobi': _('Africa/Nairobi'),
    'Antarctica/Syowa': _('Antarctica/Syowa'),
    'Asia/Aden': _('Asia/Aden'),
    'Asia/Baghdad': _('Asia/Baghdad'),
    'Asia/Bahrain': _('Asia/Bahrain'),
    'Asia/Kuwait': _('Asia/Kuwait'),
    'Asia/Qatar': _('Asia/Qatar'),
    'Asia/Riyadh': _('Asia/Riyadh'),
    'Europe/Kaliningrad': _('Europe/Kaliningrad'),
    'Indian/Antananarivo': _('Indian/Antananarivo'),
    'Indian/Comoro': _('Indian/Comoro'),
    'Indian/Mayotte': _('Indian/Mayotte'),
    'Asia/Tehran': _('Asia/Tehran'),
    'Asia/Baku': _('Asia/Baku'),
    'Asia/Dubai': _('Asia/Dubai'),
    'Asia/Muscat': _('Asia/Muscat'),
    'Asia/Tbilisi': _('Asia/Tbilisi'),
    'Asia/Yerevan': _('Asia/Yerevan'),
    'Europe/Moscow': _('Europe/Moscow'),
    'Europe/Samara': _('Europe/Samara'),
    'Europe/Volgograd': _('Europe/Volgograd'),
    'Indian/Mahe': _('Indian/Mahe'),
    'Indian/Mauritius': _('Indian/Mauritius'),
    'Indian/Reunion': _('Indian/Reunion'),
    'Asia/Kabul': _('Asia/Kabul'),
    'Antarctica/Mawson': _('Antarctica/Mawson'),
    'Asia/Aqtau': _('Asia/Aqtau'),
    'Asia/Aqtobe': _('Asia/Aqtobe'),
    'Asia/Ashgabat': _('Asia/Ashgabat'),
    'Asia/Dushanbe': _('Asia/Dushanbe'),
    'Asia/Karachi': _('Asia/Karachi'),
    'Asia/Oral': _('Asia/Oral'),
    'Asia/Samarkand': _('Asia/Samarkand'),
    'Asia/Tashkent': _('Asia/Tashkent'),
    'Indian/Kerguelen': _('Indian/Kerguelen'),
    'Indian/Maldives': _('Indian/Maldives'),
    'Asia/Colombo': _('Asia/Colombo'),
    'Asia/Kolkata': _('Asia/Kolkata'),
    'Asia/Kathmandu': _('Asia/Kathmandu'),
    'Antarctica/Vostok': _('Antarctica/Vostok'),
    'Asia/Almaty': _('Asia/Almaty'),
    'Asia/Bishkek': _('Asia/Bishkek'),
    'Asia/Dhaka': _('Asia/Dhaka'),
    'Asia/Qyzylorda': _('Asia/Qyzylorda'),
    'Asia/Thimphu': _('Asia/Thimphu'),
    'Asia/Yekaterinburg': _('Asia/Yekaterinburg'),
    'Indian/Chagos': _('Indian/Chagos'),
    'Asia/Rangoon': _('Asia/Rangoon'),
    'Indian/Cocos': _('Indian/Cocos'),
    'Antarctica/Davis': _('Antarctica/Davis'),
    'Asia/Bangkok': _('Asia/Bangkok'),
    'Asia/Ho_Chi_Minh': _('Asia/Ho_Chi_Minh'),
    'Asia/Hovd': _('Asia/Hovd'),
    'Asia/Jakarta': _('Asia/Jakarta'),
    'Asia/Novokuznetsk': _('Asia/Novokuznetsk'),
    'Asia/Novosibirsk': _('Asia/Novosibirsk'),
    'Asia/Omsk': _('Asia/Omsk'),
    'Asia/Phnom_Penh': _('Asia/Phnom_Penh'),
    'Asia/Pontianak': _('Asia/Pontianak'),
    'Asia/Vientiane': _('Asia/Vientiane'),
    'Indian/Christmas': _('Indian/Christmas'),
    'Antarctica/Casey': _('Antarctica/Casey'),
    'Asia/Brunei': _('Asia/Brunei'),
    'Asia/Choibalsan': _('Asia/Choibalsan'),
    'Asia/Chongqing': _('Asia/Chongqing'),
    'Asia/Harbin': _('Asia/Harbin'),
    'Asia/Hebron': _('Asia/Hebron'),
    'Asia/Hong_Kong': _('Asia/Hong_Kong'),
    'Asia/Kashgar': _('Asia/Kashgar'),
    'Asia/Krasnoyarsk': _('Asia/Krasnoyarsk'),
    'Asia/Kuala_Lumpur': _('Asia/Kuala_Lumpur'),
    'Asia/Kuching': _('Asia/Kuching'),
    'Asia/Macau': _('Asia/Macau'),
    'Asia/Makassar': _('Asia/Makassar'),
    'Asia/Manila': _('Asia/Manila'),
    'Asia/Shanghai': _('Asia/Shanghai'),
    'Asia/Singapore': _('Asia/Singapore'),
    'Asia/Taipei': _('Asia/Taipei'),
    'Asia/Ulaanbaatar': _('Asia/Ulaanbaatar'),
    'Asia/Urumqi': _('Asia/Urumqi'),
    'Australia/Perth': _('Australia/Perth'),
    'Australia/Eucla': _('Australia/Eucla'),
    'Asia/Dili': _('Asia/Dili'),
    'Asia/Irkutsk': _('Asia/Irkutsk'),
    'Asia/Jayapura': _('Asia/Jayapura'),
    'Asia/Pyongyang': _('Asia/Pyongyang'),
    'Asia/Seoul': _('Asia/Seoul'),
    'Asia/Tokyo': _('Asia/Tokyo'),
    'Pacific/Palau': _('Pacific/Palau'),
    'Australia/Darwin': _('Australia/Darwin'),
    'Antarctica/DumontDUrville': _('Antarctica/DumontDUrville'),
    'Asia/Yakutsk': _('Asia/Yakutsk'),
    'Australia/Brisbane': _('Australia/Brisbane'),
    'Australia/Lindeman': _('Australia/Lindeman'),
    'Pacific/Chuuk': _('Pacific/Chuuk'),
    'Pacific/Guam': _('Pacific/Guam'),
    'Pacific/Port_Moresby': _('Pacific/Port_Moresby'),
    'Pacific/Saipan': _('Pacific/Saipan'),
    'Australia/Adelaide': _('Australia/Adelaide'),
    'Australia/Broken_Hill': _('Australia/Broken_Hill'),
    'Antarctica/Macquarie': _('Antarctica/Macquarie'),
    'Asia/Sakhalin': _('Asia/Sakhalin'),
    'Asia/Vladivostok': _('Asia/Vladivostok'),
    'Australia/Currie': _('Australia/Currie'),
    'Australia/Hobart': _('Australia/Hobart'),
    'Australia/Lord_Howe': _('Australia/Lord_Howe'),
    'Australia/Melbourne': _('Australia/Melbourne'),
    'Australia/Sydney': _('Australia/Sydney'),
    'Pacific/Efate': _('Pacific/Efate'),
    'Pacific/Guadalcanal': _('Pacific/Guadalcanal'),
    'Pacific/Kosrae': _('Pacific/Kosrae'),
    'Pacific/Noumea': _('Pacific/Noumea'),
    'Pacific/Pohnpei': _('Pacific/Pohnpei'),
    'Pacific/Norfolk': _('Pacific/Norfolk'),
    'Asia/Anadyr': _('Asia/Anadyr'),
    'Asia/Kamchatka': _('Asia/Kamchatka'),
    'Asia/Magadan': _('Asia/Magadan'),
    'Pacific/Fiji': _('Pacific/Fiji'),
    'Pacific/Funafuti': _('Pacific/Funafuti'),
    'Pacific/Kwajalein': _('Pacific/Kwajalein'),
    'Pacific/Majuro': _('Pacific/Majuro'),
    'Pacific/Nauru': _('Pacific/Nauru'),
    'Pacific/Tarawa': _('Pacific/Tarawa'),
    'Pacific/Wake': _('Pacific/Wake'),
    'Pacific/Wallis': _('Pacific/Wallis'),
    'Antarctica/McMurdo': _('Antarctica/McMurdo'),
    'Antarctica/South_Pole': _('Antarctica/South_Pole'),
    'Pacific/Auckland': _('Pacific/Auckland'),
    'Pacific/Enderbury': _('Pacific/Enderbury'),
    'Pacific/Tongatapu': _('Pacific/Tongatapu'),
    'Pacific/Chatham': _('Pacific/Chatham'),
    'Pacific/Kiritimati': _('Pacific/Kiritimati'),
}

TIMEZONE_CHOICES = []
for tz_choice in TIMEZONE_TRANSLATION:
    tz_choice_translated = (tz_choice, TIMEZONE_TRANSLATION[tz_choice])
    TIMEZONE_CHOICES.append(tz_choice_translated)
TIMEZONE_CHOICES.sort()