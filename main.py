from bs4 import BeautifulSoup
import requests

apple_links = {
    'GLOBAL' : 'https://music.apple.com/us/playlist/top-100-global/pl.d25f5d1181894928af76c85c967f8f31',
    # United States and Canada
    'US' : 'https://music.apple.com/us/playlist/top-100-usa/pl.606afcbb70264d2eb2b51d8dbcfa6a12',
    'CA' : 'https://music.apple.com/us/playlist/top-100-canada/pl.79bac9045a2540e0b195e983df8ba569',
    # Latin America and the Caribbean
    'AI' : 'https://music.apple.com/us/playlist/top-100-anguilla/pl.48bbe91b5d944b0aa7b1e90a3889b6a7',
    'CO' : 'https://music.apple.com/us/playlist/top-100-colombia/pl.d116fa6286734b74acff3d38a740fe0d',
    'AG' : 'https://music.apple.com/us/playlist/top-100-antigua-and-barbuda/pl.cca0d50798424e4e871820a03719e841',
    'NI' : 'https://music.apple.com/us/playlist/top-100-nicaragua/pl.2249e0cc6edb46f4ae64de2c937a4f41',
    'CR' : 'https://music.apple.com/us/playlist/top-100-costa-rica/pl.7771c20fc0354f64a723ae9c11a4d5f5',
    'PA' : 'https://music.apple.com/us/playlist/top-100-panama/pl.9d5ee7c72f804dbab97163616c7a8399',
    'AR' : 'https://music.apple.com/us/playlist/top-100-argentina/pl.7ae8594e422f44658e58212d876d9323',
    'DM' : 'https://music.apple.com/us/playlist/top-100-dominica/pl.68e6ad675521400487ea78463b39899d',
    'PY' : 'https://music.apple.com/ng/playlist/top-100-paraguay/pl.0843e61953c1430287162e5a36dff52b',
    'DO' : 'https://music.apple.com/us/playlist/top-100-dominican-republic/pl.deec8b036583481782c40a2a05554b0b',
    'PE' : 'https://music.apple.com/us/playlist/top-100-peru/pl.569a0034bcc64db68bb13afa8171a687',
    'EC' : 'https://music.apple.com/us/playlist/top-100-ecuador/pl.41b0d399afea495699dbc7660994a96c',
    'BB' : 'https://music.apple.com/us/playlist/top-100-barbados/pl.13743dcd86174ea5b4cb6b2534637e23',
    'KN' : 'https://music.apple.com/us/playlist/top-100-st-kitts-and-nevis/pl.be7b2d63abaf4d25918ef41187f88be4',
    'BZ' : 'https://music.apple.com/us/playlist/top-100-belize/pl.c6d8b5dcf6814168a4b0262628d3a317',
    'SV' : 'https://music.apple.com/ng/playlist/top-100-el-salvador/pl.9a175d1e9b1e4c81bfa7c63f28c1a79e',
    'BM' : 'https://music.apple.com/us/playlist/top-100-bermuda/pl.b0cc7d688aa94588a640412c9686bf1b',
    'GD' : 'https://music.apple.com/us/playlist/top-100-grenada/pl.b14c0257c1744d2686f88d05ab1efb4c',
    'BO' : 'https://music.apple.com/us/playlist/top-100-bolivia/pl.cfcd547b034d47648a16fb8e2df0623f',
    'GT' : 'https://music.apple.com/us/playlist/top-100-guatemala/pl.7235b4236ee241f083f8026d372cc2d8',
    'TT' : 'https://music.apple.com/us/playlist/top-100-trinidad-and-tobago/pl.f1495be1a9774341ab8a1eceb7011579',
    'BR' : 'https://music.apple.com/us/playlist/top-100-brazil/pl.11ac7cc7d09741c5822e8c66e5c7edbb',
    'HN' : 'https://music.apple.com/us/playlist/top-100-honduras/pl.ec6d493f976349dfb0cba8f6c2f7e937',
    'VG' : 'https://music.apple.com/us/playlist/top-100-british-virgin-islands/pl.d4b2fe66a810440186c27434fa71072a',
    'KY' : 'https://music.apple.com/us/playlist/top-100-cayman-islands/pl.c5a087a907dc44dfbbbd2f471f16a467',
    'MX' : 'https://music.apple.com/us/playlist/top-100-mexico/pl.df3f10ca27b1479087de2cd3f9f6716b',
    'VE' : 'https://music.apple.com/us/playlist/top-100-venezuela/pl.617da0e0bbb74461b607cad435b1e941',
    'CL' : 'https://music.apple.com/us/playlist/top-100-chile/pl.81015bbbefdd46758b2c8c7065f0863e',
    # Europe, Russia, and Central Asia
    'HU' : 'https://music.apple.com/us/playlist/top-100-hungary/pl.cee165c3a51e466481bde5de75d6dee3',
    'PL' : 'https://music.apple.com/us/playlist/top-100-poland/pl.8c91cbb0ef4e48308dbbba4238135eaf',
    'AT' : 'https://music.apple.com/us/playlist/top-100-austria/pl.f34430d010a843128337927bba98048b',
    'PT' : 'https://music.apple.com/il/playlist/top-100-portugal/pl.5437c1490ac74e9e9505fc7d1f201655',
    'IE' : 'https://music.apple.com/gb/playlist/top-100-ireland/pl.3b47111ed6b7461eae67fadf895d56db',
    'BY' : 'https://music.apple.com/us/playlist/top-100-belarus/pl.50c1747c37404a9aa07acc39316f6873',
    'RO' : 'https://music.apple.com/us/playlist/top-100-romania/pl.0c6bea611ad54c79b854299bc515a5a6',
    'RU' : 'https://music.apple.com/us/playlist/top-100-russia/pl.728bd30a9247487c80a483f4168a9dcd',
    'IT' : 'https://music.apple.com/us/playlist/top-100-italy/pl.737e067787df485a8062e2c4927d94db',
    'BE' : 'https://music.apple.com/id/playlist/top-100-belgium/pl.cefe84f7916b4cae8b21b0a78e948380',
    'KZ' : 'https://music.apple.com/us/playlist/top-100-kazakhstan/pl.27d3c4d63b0e41f29f79c98bb5a090e1',
    'BG' : 'https://music.apple.com/us/playlist/top-100-bulgaria/pl.040cf0b4c7e9467eb9eed2d33e7a29d6',
    'SK' : 'https://music.apple.com/us/playlist/top-100-slovakia/pl.2e50996a5bf44ab78cbb5c34b1992701',
    'KG' : 'https://music.apple.com/us/playlist/top-100-kyrgyzstan/pl.5318aa72adb84bcfac803ecaf6156325',
    'SI' : 'https://music.apple.com/us/playlist/top-100-slovenia/pl.e7374de32aec446c92136234d5bcae2f',
    'CY' : 'https://music.apple.com/us/playlist/top-100-cyprus/pl.a5ae21745d1d45edacb68971746d31ae',
    'LV' : 'https://music.apple.com/us/playlist/top-100-latvia/pl.5ac047a9ada144aebb9b2f16f5bc8c1d',
    'ES' : 'https://music.apple.com/kg/playlist/top-100-spain/pl.0d656d7feae64198bc5fb1b02786ed75',
    'CZ' : 'https://music.apple.com/us/playlist/top-100-czech-republic/pl.e447d9ba54254130a76143bf6fdfa65c',
    'LT' : 'https://music.apple.com/us/playlist/top-100-lithuania/pl.e96de57d836e42dca30f7da24c64bbea',
    'SE' : 'https://music.apple.com/lu/playlist/top-100-sweden/pl.5876877c387b4ffb8860ac3ea2c244c3',
    'DK' : 'https://music.apple.com/us/playlist/top-100-denmark/pl.d08496850bc840a4874e877177a69f9f',
    'LU' : 'https://music.apple.com/us/playlist/top-100-luxembourg/pl.2f85377267d74a13be02a53882a5b488',
    'CH' : 'https://music.apple.com/us/playlist/top-100-switzerland/pl.bb1f5218a0f04de3877c4f9ccd63d260',
    'EE' : 'https://music.apple.com/us/playlist/top-100-estonia/pl.054734b06c7742a985805f45a283bcb4',
    'MT' : 'https://music.apple.com/us/playlist/top-100-malta/pl.06ab782ba2324ae49317d6bde84eef56',
    'TJ' : 'https://music.apple.com/us/playlist/top-100-tajikistan/pl.ea75568dc0524a479b818d551a7b3c35',
    'FI' : 'https://music.apple.com/us/playlist/top-100-finland/pl.acea41a017664a8ebcd5aa1622aecc88',
    'MD' : 'https://music.apple.com/il/playlist/top-100-moldova/pl.e4dcd4663130419bb03b80216dee9f57',
    'TM' : 'https://music.apple.com/us/playlist/top-100-turkmenistan/pl.f783d8aec4df401583434a2454adbc3d',
    'FR' : 'https://music.apple.com/us/playlist/top-100-france/pl.6e8cfd81d51042648fa36c9df5236b8d',
    'NL' : 'https://music.apple.com/us/playlist/top-100-netherlands/pl.26fb1998d54a4b3192be548529a97f8e',
    'UA' : 'https://music.apple.com/us/playlist/top-100-ukraine/pl.815f78effb3844909a8259d759ecbddb',
    'DE' : 'https://music.apple.com/us/playlist/top-100-germany/pl.c10a2c113db14685a0b09fa5834d8e8b',
    'UK' : 'https://music.apple.com/us/playlist/top-100-uk/pl.c2273b7e89b44121b3093f67228918e7',
    'NO' : 'https://music.apple.com/us/playlist/top-100-norway/pl.05a67957c3974729aac67c01247e55b6',
    'GR' : 'https://music.apple.com/us/playlist/top-100-greece/pl.0f15f3a8ba014979b9fdd7a0ef906dca',
    'UZ' : 'https://music.apple.com/us/playlist/top-100-uzbekistan/pl.90ad69a600ed4d10b00d158eea68cad7',
    # Africa 
    'GM' : 'https://music.apple.com/us/playlist/top-100-gambia/pl.62e12ecd522d47858321846adcaac43d',
    'NG' : 'https://music.apple.com/ca/playlist/top-100-nigeria/pl.2fc68f6d68004ae993dadfe99de83877',
    'GW' : 'https://music.apple.com/us/playlist/top-100-guinea-bissau/pl.ac455234996b468b9f58e573752ab05c',
    'KE' : 'https://music.apple.com/gb/playlist/top-100-kenya/pl.0b36ea82865d4adeb9d1d62207aab172',
    'BW' : 'https://music.apple.com/tr/playlist/top-100-botswana/pl.73bb3593281444fb8ab21d58ccab4600',
    'CV' : 'https://music.apple.com/us/playlist/top-100-cape-verde/pl.917f294713a34cdeb46e67ad2a137067',
    'ZA' : 'https://music.apple.com/za/playlist/top-100-south-africa/pl.447bd05172824b89bd745628f7f54c18',
    'MU' : 'https://music.apple.com/us/playlist/top-100-mauritius/pl.5e6efed969354b378770c2ea6f2fed6b',
    'MA' : 'https://music.apple.com/us/playlist/top-100-morocco/pl.u-yZyVVjxTZy7NLV',
    'UG' : 'https://music.apple.com/us/playlist/top-100-uganda/pl.b9e553253ed24c2a829c9c08209e5f67',
    'SZ' : 'https://music.apple.com/gb/playlist/top-100-swaziland/pl.046c3e297666475aa84c12159a954596',
    'ZW' : 'https://music.apple.com/us/playlist/top-100-zimbabwe/pl.ad37160bb16c4c70a1d83d3670e96c1a',
    'GH' : 'https://music.apple.com/ca/playlist/top-100-ghana/pl.78f1974e882d4952b26ebfb8e017c933',
    # Asia-Pacific
    'AU' : 'https://music.apple.com/us/playlist/top-100-australia/pl.18be1cf04dfd4ffb9b6b0453e8fae8f1',
    'LA' : 'https://music.apple.com/us/playlist/top-100-laos/pl.42b3fe9c75a947ab84a80019e7bcd704',
    'PG' : 'https://music.apple.com/us/playlist/top-100-papua-new-guinea/pl.30fbe54afbf846edabdbe00e90095d04',
    'PH' : 'https://music.apple.com/us/playlist/top-100-philippines/pl.b9eb00f9d195440e8b0bdf19b8db7f34',
    'MO' : 'https://music.apple.com/ca/playlist/top-100-macau/pl.28e8a715012b4ed9b9527100da1e3474',
    'SG': 'https://music.apple.com/cy/playlist/top-100-singapore/pl.4d763fa1cf15433b9994a14be6a46164', 
    'MY' : 'https://music.apple.com/in/playlist/top-100-malaysia/pl.a165defeeccb4b17a59bb5c85637b9b7',
    'KH' : 'https://music.apple.com/us/playlist/top-100-cambodia/pl.9d9ee12c7734402ab5ab0dc81911822c',
    'FM' : 'https://music.apple.com/us/playlist/top-100-micronesia/pl.bee910bc105b43c28eed7d20e4e09a8c',
    'KR' : 'https://music.apple.com/us/playlist/top-100-south-korea/pl.d3d10c32fbc540b38e266367dc8cb00c',
    'CN' : 'https://music.apple.com/us/playlist/top-100-china/pl.fde851dc95ce4ffbb74028dfd254ced5',
    'FJ' : 'https://music.apple.com/ca/playlist/top-100-fiji/pl.1e2c1286034c49b78139d2b4ff499a94',
    'MN' : 'https://music.apple.com/eg/playlist/top-100-mongolia/pl.71c450d15a9e4440ac5d24c174958225',
    'LK' : 'https://music.apple.com/us/playlist/top-100-sri-lanka/pl.cd9b6c35086b43b193ecc3d32882a41e',
    'HK' : 'https://music.apple.com/us/playlist/top-100-hong-kong/pl.7f35cffa10b54b91aab128ccc547f6ef',
    'TW' : 'https://music.apple.com/sg/playlist/top-100-taiwan/pl.741ff34016704547853b953ec5181d83',
    'IN' : 'https://music.apple.com/tr/playlist/top-100-india/pl.c0e98d2423e54c39b3df955c24df3cc5',
    'NP' : 'https://music.apple.com/tr/playlist/top-100-nepal/pl.9032e70a644e442688f120a829c636cd',
    'TH' : 'https://music.apple.com/us/playlist/top-100-thailand/pl.c509137d97214632a087129ece060a3d',
    'ID' : 'https://music.apple.com/us/playlist/top-100-indonesia/pl.2b7e089dc9ef4dd7a18429df9c6e26a3',
    'NZ' : 'https://music.apple.com/us/playlist/top-100-new-zealand/pl.d8742df90f43402ba5e708eefd6d949a',
    'JP' : 'https://music.apple.com/us/playlist/top-100-japan/pl.043a2c9876114d95a4659988497567be',
    'VT' : 'https://music.apple.com/us/playlist/top-100-vietnam/pl.550110ec6feb4ae0aff364bcde6d1372',
    # Middle East
    'IL' : 'https://music.apple.com/us/playlist/top-100-israel/pl.0c9765e5330048af96c2336fa7bc3525',
    'AM' : 'https://music.apple.com/ke/playlist/top-100-armenia/pl.42abb2144d594137a8fb4d37a9f35b42',
    'SA' : 'https://music.apple.com/us/playlist/top-100-saudi-arabia/pl.a5365fa3b6ec4a34994339ca100801ae',
    'JO' : 'https://music.apple.com/us/playlist/top-100-jordan/pl.5adf310412994d9483918fcd8e091fc5',
    'AZ' : 'https://music.apple.com/us/playlist/top-100-azerbaijan/pl.ccc31c81303c405baddaaf0f5328b7f3',
    'TR' : 'https://music.apple.com/tr/playlist/top-100-turkey/pl.f3e0d6ef238542609572c18b0de1513b',
    'BH' : 'https://music.apple.com/us/playlist/top-100-bahrain/pl.02a8276fa4ca40b19ac248fda4725fbb',
    'LB' : 'https://music.apple.com/us/playlist/top-100-lebanon/pl.838a4daba8924c42969ca7162fdc74da',
    'AE' : 'https://music.apple.com/us/playlist/top-100-united-arab-emirates/pl.7b5e51f09aee4733958e23ea97dda459',
    'EG' : 'https://music.apple.com/us/playlist/top-100-egypt/pl.a0b3d0b9a2764646b59ccacdf82e3544',
    'OM' : 'https://music.apple.com/us/playlist/top-100-oman/pl.d4ca5698caf04a9f873861c3659aeeca',
}
for country, links in apple_links.items():
    print(country)
    source = requests.get(links).text

    soup = BeautifulSoup(source, 'lxml')

    songs = []

    count = 0
    for count, song in enumerate(soup.find_all('div', class_='songs-list-row__song-name')):
        song.append(str(count + 1) + '. ' + song.text)

    # isAlbum if False
    isAlbum = False
    index = 0
    for index, artist_album in enumerate(soup.find_all('div', class_='songs-list__song-link-wrapper')):
        print(index)
        # if (isAlbum):
        #     isAlbum = False
        #     continue
        # else:
        #     originalText = (artist_album.text).split()
        #     songs[index] = songs[index] + " by " + " ".join(originalText).replace(" ,", ",")
        #     isAlbum = True
    
    print(songs[0:100])

    print()
    print()
    print()
    print()
    print()
    print()


# for song in soup.find_all('div', class_='songs-list-row songs-list-row--web-preview web-preview songs-list-row--two-lines songs-list-row--song'):
#     print(song)