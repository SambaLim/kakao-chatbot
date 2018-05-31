# 지역의 코드를 저장하고 불러올 수 있게함.

region_dict = {
			# 특별시, 광역시
			'인천':11200510,
			'인천광역시':11200510,
			'인천시':11200510,
			'서울':09140550,
			'서울특별시':09140550,
			'서울시':09140550,
			'대전':07170630,
			'대전광역시':07170630,
			'대전시':07170630,
			'대구':06110517,
			'대구광역시':06110517,
			'대구시':06110517,
			'부산':08470690,
			'부산광역시':08470690,
			'부산시':08470690,
			'광주':05140120,
			'광주광역시':05140120,
			'광주시':05140120,
			'울산':10140510,
			'울산광역시':10140510,
			'울산시':10140510,
			'세종':17110250,
			
			# 도
			'경기':02830410,
			'경기도':02830410,
			'강원':01810350,
			'강원도':01810350,
			'충청북도':16760370,
			'충북':16760370,
			'충청남도':15810320,
			'충남':15810320,
			'전라북도':13750360,
			'전북':13750360,
			'전라남도':12790330,
			'전남':12790330,
			'경상북도':04170400,
			'경북':04170400,
			'경상남도':03720415,
			'경남':03720415,
			'제주도':14110630,
			'제주':14110630
 
		}


def get_region_code(string):
	regionCode = region_dict[string]
	return regionCode
	