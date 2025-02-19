import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import plotly.express as px

# Sample data for the map
df = px.data.gapminder().query("year == 2007")

# Create a plain world map figure
fig = px.choropleth(df, locations="iso_alpha", hover_name="country", projection="mercator")
fig.update_geos(showcoastlines=True, coastlinecolor="black")  # Show coastlines
fig.update_traces(marker=dict(line=dict(color="black", width=0.5)))  # Country borders in black
fig.update_layout(
    coloraxis_showscale=False,  # Hide color scale
    geo=dict(bgcolor='rgba(0,0,0,0)') # Transparent background
)
fig.update_layout(width=900, height=800)  # Set map size for 75% width

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

country_adaptations = {
    "Australia": {
        "Adaptation Mechanisms": "High melanin production among indigenous populations to protect against intense UV radiation.",
        "Historical Context": "Aboriginal Australians developed darker skin suited to intense sun exposure, while recent settlers have lighter skin.",
        "Modern Challenges": "Vitamin D deficiency in urbanized populations due to indoor lifestyles.",
        "Exceptions": "Light-skinned populations more susceptible to UV damage.",
        "Impact of Lifestyle": "High sunscreen usage and public health campaigns promote sun safety."
    },
    "Brazil": {
        "Adaptation Mechanisms": "Diverse skin pigmentation due to varied ancestry and UV exposure in different regions.",
        "Historical Context": "Indigenous populations adapted to high UV areas, with lighter-skinned European descendants in the south.",
        "Modern Challenges": "Urbanization impacts natural UV exposure and increases skin cancer rates in lighter-skinned populations.",
        "Exceptions": "Some regions see increased health disparities based on pigmentation.",
        "Impact of Lifestyle": "Public awareness campaigns for sunscreen and UV protection are prevalent."
    },
    "Canada": {
        "Adaptation Mechanisms": "Lower melanin levels in indigenous and European-descended populations for vitamin D synthesis in low UV areas.",
        "Historical Context": "Lighter skin tones evolved due to low UV exposure and long winters.",
        "Modern Challenges": "Vitamin D deficiency is common due to lack of natural sunlight.",
        "Exceptions": "Immigrant populations with darker skin may face higher vitamin D deficiency risks.",
        "Impact of Lifestyle": "Supplementation and fortified foods address vitamin D deficiency concerns."
    },
    "Kenya": {
        "Adaptation Mechanisms": "Higher melanin levels among native populations as protection from equatorial UV radiation.",
        "Historical Context": "Dark skin tones evolved to protect against intense UV exposure near the equator.",
        "Modern Challenges": "Increased urbanization has led to reduced natural UV exposure.",
        "Exceptions": "People with albinism are at increased risk of UV-related health issues.",
        "Impact of Lifestyle": "Education on sunscreen and protective clothing is increasing in urban areas."
    },
    "Norway": {
        "Adaptation Mechanisms": "Lower melanin levels to maximize vitamin D synthesis in low UV conditions.",
        "Historical Context": "Lighter skin tones became common in response to low UV exposure.",
        "Modern Challenges": "Higher skin cancer risks during short summer months with increased sun exposure.",
        "Exceptions": "Immigrants with darker skin face vitamin D deficiency.",
        "Impact of Lifestyle": "Vitamin D supplementation is common in regions with low UV exposure."
    },
    "India": {
        "Adaptation Mechanisms": "Varied pigmentation levels; higher melanin levels in southern regions due to intense sunlight.",
        "Historical Context": "Dark pigmentation evolved to protect against UV radiation in tropical areas.",
        "Modern Challenges": "Urban migration reduces natural sunlight exposure.",
        "Exceptions": "Northern populations have lighter pigmentation compared to southern populations.",
        "Impact of Lifestyle": "Vitamin D deficiency is a growing concern in urban areas."
    },
    "Japan": {
        "Adaptation Mechanisms": "Moderate melanin levels suited to temperate UV levels.",
        "Historical Context": "Skin tone adapted to moderate UV exposure, lighter in the north, darker in the south.",
        "Modern Challenges": "Urban lifestyles contribute to vitamin D deficiency.",
        "Exceptions": "Higher skin cancer rates among fair-skinned individuals.",
        "Impact of Lifestyle": "Awareness of UV protection is increasing, with a focus on vitamin D."
    },
    "South Africa": {
        "Adaptation Mechanisms": "Higher melanin levels in native populations for UV protection.",
        "Historical Context": "Populations adapted to intense sun exposure in certain regions.",
        "Modern Challenges": "Shift to indoor work increases vitamin D deficiency.",
        "Exceptions": "Immigrant populations from low UV areas may have higher skin cancer risks.",
        "Impact of Lifestyle": "Public health campaigns promote sunscreen use and vitamin D awareness."
    },
    "Russia": {
        "Adaptation Mechanisms": "Low melanin levels to maximize vitamin D synthesis in low UV regions.",
        "Historical Context": "Lighter skin tones evolved in response to low UV radiation in northern areas.",
        "Modern Challenges": "Risk of vitamin D deficiency due to limited sunlight exposure.",
        "Exceptions": "Ethnic diversity in southern regions with darker skin tones.",
        "Impact of Lifestyle": "Widespread vitamin D supplementation is encouraged in low-sun regions."
    },
    "Mexico": {
        "Adaptation Mechanisms": "Moderate to dark pigmentation adapted to varied UV levels across the country.",
        "Historical Context": "Indigenous populations developed darker skin in areas with high UV exposure.",
        "Modern Challenges": "Urbanization reduces natural UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Fair-skinned descendants of Europeans more susceptible to UV damage.",
        "Impact of Lifestyle": "Sunscreen and sun protection are emphasized in high UV regions."
    },
    "Argentina": {
        "Adaptation Mechanisms": "Diverse pigmentation due to mixed ancestry and varied UV exposure.",
        "Historical Context": "Indigenous populations adapted to UV levels in different parts of the country.",
        "Modern Challenges": "Vitamin D deficiency is increasing in urban populations.",
        "Exceptions": "Light-skinned European descendants at higher risk of UV damage.",
        "Impact of Lifestyle": "Public health initiatives focus on sunscreen and vitamin D awareness."
    },
    "Indonesia": {
        "Adaptation Mechanisms": "Higher melanin levels to protect against equatorial UV radiation.",
        "Historical Context": "Darker skin tones evolved as a defense against intense sun exposure.",
        "Modern Challenges": "Urbanization has led to reduced natural sunlight exposure.",
        "Exceptions": "Lighter-skinned populations from higher altitudes may face more UV exposure challenges.",
        "Impact of Lifestyle": "Increasing public awareness about sunscreen and sun safety."
    },
    "Spain": {
        "Adaptation Mechanisms": "Moderate melanin levels suited to Mediterranean UV exposure.",
        "Historical Context": "Mixed heritage with influences from Europe and North Africa.",
        "Modern Challenges": "Skin cancer rates rising among fair-skinned individuals.",
        "Exceptions": "Vitamin D deficiency in elderly populations due to reduced sunlight exposure.",
        "Impact of Lifestyle": "Growing use of sunscreen and increased awareness of UV protection."
    },
    "Egypt": {
        "Adaptation Mechanisms": "Dark skin tones evolved in indigenous populations to cope with intense sun exposure.",
        "Historical Context": "Long history of adaptation to desert UV levels.",
        "Modern Challenges": "Urbanization has reduced natural sunlight exposure for many.",
        "Exceptions": "People with lighter skin are at a higher risk of UV damage.",
        "Impact of Lifestyle": "Public health campaigns promote sunscreen and shade use in urban areas."
    },
    "United Kingdom": {
        "Adaptation Mechanisms": "Lower melanin levels to allow for maximum vitamin D synthesis.",
        "Historical Context": "Lighter skin tones evolved due to limited sunlight and low UV exposure.",
        "Modern Challenges": "Vitamin D deficiency is common in winter due to limited sunlight.",
        "Exceptions": "Recent immigrant populations face higher risks of vitamin D deficiency.",
        "Impact of Lifestyle": "Widespread use of vitamin D supplements during winter months."
    },
    "Italy": {
        "Adaptation Mechanisms": "Moderate pigmentation suitable for Mediterranean climate.",
        "Historical Context": "Adapted to varied UV exposure across the northern and southern regions.",
        "Modern Challenges": "Increased skin cancer risk in northern populations with fair skin.",
        "Exceptions": "Darker skin tones in southern Italy adapted to higher UV levels.",
        "Impact of Lifestyle": "Rising awareness about sunscreen and vitamin D supplementation."
    },
    # Additional countries can follow a similar format...
}

country_adaptations.update({
    "China": {
        "Adaptation Mechanisms": "Varied melanin levels; northern populations lighter-skinned, southern populations darker.",
        "Historical Context": "Diverse skin tones evolved based on regional UV exposure.",
        "Modern Challenges": "Urban lifestyles and air pollution limit natural UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Rural populations retain more traditional sun exposure habits.",
        "Impact of Lifestyle": "Increased use of vitamin D supplements and fortified foods in urban areas."
    },
    "Nigeria": {
        "Adaptation Mechanisms": "High melanin levels provide natural UV protection in tropical climates.",
        "Historical Context": "Darker pigmentation evolved as a defense against intense UV radiation.",
        "Modern Challenges": "Migration to cities and indoor jobs reduce natural UV exposure.",
        "Exceptions": "Populations with albinism are particularly vulnerable to UV damage.",
        "Impact of Lifestyle": "Growing awareness of sunscreen and vitamin D deficiency in urban settings."
    },
    "Sweden": {
        "Adaptation Mechanisms": "Lower melanin levels maximize vitamin D synthesis in low UV environments.",
        "Historical Context": "Lighter skin evolved due to low sunlight, especially in winter.",
        "Modern Challenges": "Vitamin D deficiency is prevalent in the winter months.",
        "Exceptions": "Immigrants from high UV areas face increased risks of vitamin D deficiency.",
        "Impact of Lifestyle": "Vitamin D supplementation is common, especially during winter."
    },
    "Turkey": {
        "Adaptation Mechanisms": "Moderate melanin levels adapted to Mediterranean climate.",
        "Historical Context": "Ancient populations adapted to varied UV levels across Anatolia.",
        "Modern Challenges": "Increasing cases of vitamin D deficiency in urban areas.",
        "Exceptions": "People with lighter skin tones face higher UV risks in southern Turkey.",
        "Impact of Lifestyle": "Public awareness on sun protection is rising in high UV regions."
    },
    "Iran": {
        "Adaptation Mechanisms": "Varied pigmentation from darker skin in the south to lighter skin in the north.",
        "Historical Context": "Adaptations to desert UV levels and mountainous regions.",
        "Modern Challenges": "Urbanization reduces natural UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Mountain populations often experience more intense UV exposure.",
        "Impact of Lifestyle": "Increased use of vitamin D supplements in urban areas."
    },
    "Saudi Arabia": {
        "Adaptation Mechanisms": "High melanin levels in indigenous populations adapted to intense desert UV.",
        "Historical Context": "Adapted to harsh, sunny conditions in desert regions.",
        "Modern Challenges": "Vitamin D deficiency is prevalent due to limited sun exposure and cultural clothing practices.",
        "Exceptions": "Lighter-skinned individuals more vulnerable to UV damage.",
        "Impact of Lifestyle": "Vitamin D supplements and fortified foods are increasingly common."
    },
    "Israel": {
        "Adaptation Mechanisms": "Moderate pigmentation adapted to Mediterranean UV exposure.",
        "Historical Context": "Ancient populations developed pigmentation suited to sunny climates.",
        "Modern Challenges": "Increased skin cancer risk among light-skinned populations.",
        "Exceptions": "Immigrants from northern regions often have lighter skin, higher UV risks.",
        "Impact of Lifestyle": "Sunscreen use and awareness campaigns focus on UV protection."
    },
    "Peru": {
        "Adaptation Mechanisms": "Higher melanin levels in Andean and Amazon populations for UV protection.",
        "Historical Context": "Dark pigmentation evolved due to high UV exposure at altitude and in tropical regions.",
        "Modern Challenges": "Vitamin D deficiency in urban areas and coastal populations.",
        "Exceptions": "Darker skin in high-altitude populations adapted to strong UV radiation.",
        "Impact of Lifestyle": "Public health efforts promote vitamin D awareness."
    },
    "Greece": {
        "Adaptation Mechanisms": "Moderate pigmentation adapted to Mediterranean sun exposure.",
        "Historical Context": "Adapted over centuries to varied UV exposure across Greece.",
        "Modern Challenges": "Rising skin cancer rates due to prolonged summer sun exposure.",
        "Exceptions": "Fair-skinned northern populations face higher UV risks.",
        "Impact of Lifestyle": "Sunscreen and sun-protection campaigns are common."
    },
    "Pakistan": {
        "Adaptation Mechanisms": "Diverse skin pigmentation across different UV zones.",
        "Historical Context": "Darker skin in southern regions, lighter skin in mountainous northern areas.",
        "Modern Challenges": "Vitamin D deficiency is common in urban settings.",
        "Exceptions": "Fair-skinned populations in the north are more vulnerable to UV damage.",
        "Impact of Lifestyle": "Increased vitamin D supplementation and fortified foods."
    },
    "Bangladesh": {
        "Adaptation Mechanisms": "Higher melanin levels provide natural UV protection.",
        "Historical Context": "Adapted to high humidity and tropical sun exposure.",
        "Modern Challenges": "Urban migration reduces natural UV exposure, leading to vitamin D issues.",
        "Exceptions": "People with albinism are highly susceptible to UV-related health risks.",
        "Impact of Lifestyle": "Increased public awareness of sunscreen and protective clothing."
    },
    "Italy": {
        "Adaptation Mechanisms": "Moderate pigmentation, with lighter skin in the north and darker in the south.",
        "Historical Context": "Adaptations to varied UV exposure across the Italian peninsula.",
        "Modern Challenges": "Increased skin cancer risks in northern populations with fair skin.",
        "Exceptions": "Higher melanin in southern populations adapted to intense sun.",
        "Impact of Lifestyle": "Growing awareness about sun safety and vitamin D deficiency."
    },
    "France": {
        "Adaptation Mechanisms": "Moderate pigmentation adapted to temperate and Mediterranean climates.",
        "Historical Context": "Mixed ancestry led to varied skin tones across France.",
        "Modern Challenges": "Higher rates of skin cancer in fair-skinned populations.",
        "Exceptions": "Immigrant populations face vitamin D deficiency issues.",
        "Impact of Lifestyle": "Sunscreen use is encouraged, with growing awareness on UV protection."
    },
    "Philippines": {
        "Adaptation Mechanisms": "Higher melanin levels in native populations to cope with intense UV.",
        "Historical Context": "Dark pigmentation evolved to provide protection from tropical UV exposure.",
        "Modern Challenges": "Urban lifestyles lead to lower natural UV exposure and vitamin D deficiency.",
        "Exceptions": "Coastal populations receive higher sun exposure compared to urban areas.",
        "Impact of Lifestyle": "Public awareness of sunscreen and vitamin D supplementation is increasing."
    },
    "Thailand": {
        "Adaptation Mechanisms": "Higher melanin levels for UV protection in tropical environments.",
        "Historical Context": "Adaptations to intense UV and humidity across Thailand.",
        "Modern Challenges": "Urbanization and reduced outdoor activities lead to vitamin D deficiency.",
        "Exceptions": "Lighter skin tones in northern populations compared to southern regions.",
        "Impact of Lifestyle": "Vitamin D awareness and sunscreen use are on the rise."
    },
    "Vietnam": {
        "Adaptation Mechanisms": "Higher melanin levels suited to tropical sun exposure.",
        "Historical Context": "Dark pigmentation evolved as a natural protection against UV.",
        "Modern Challenges": "Vitamin D deficiency due to urban lifestyles and limited sunlight.",
        "Exceptions": "Rural populations receive more natural UV exposure.",
        "Impact of Lifestyle": "Increased public health efforts on vitamin D supplementation."
    },
    "South Korea": {
        "Adaptation Mechanisms": "Moderate pigmentation adapted to temperate climate with seasonal UV changes.",
        "Historical Context": "Skin tones adapted to a range of UV levels across different regions.",
        "Modern Challenges": "Urbanization and pollution reduce natural UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Light-skinned individuals face higher skin cancer risks.",
        "Impact of Lifestyle": "Vitamin D supplements are common, with increased awareness on sun protection."
    },
    "Portugal": {
        "Adaptation Mechanisms": "Moderate pigmentation adapted to Mediterranean climate.",
        "Historical Context": "Mix of light and dark skin tones across Portugal.",
        "Modern Challenges": "Higher skin cancer risks for fair-skinned populations.",
        "Exceptions": "Southern regions have slightly darker pigmentation.",
        "Impact of Lifestyle": "Sunscreen use and sun protection awareness are common."
    },
    "Colombia": {
        "Adaptation Mechanisms": "Varied pigmentation levels across tropical and mountainous regions.",
        "Historical Context": "Adapted to both high-altitude and tropical UV levels.",
        "Modern Challenges": "Vitamin D deficiency in urban populations with reduced sunlight exposure.",
        "Exceptions": "High-altitude populations receive more intense UV exposure.",
        "Impact of Lifestyle": "Public health campaigns focus on vitamin D and sun protection."
    },
    "Morocco": {
        "Adaptation Mechanisms": "Moderate to dark skin tones adapted to desert and Mediterranean UV exposure.",
        "Historical Context": "Adapted to intense sunlight in desert areas and moderate exposure near the coast.",
        "Modern Challenges": "Urbanization reduces outdoor UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Fair-skinned populations face more sun-related health risks.",
        "Impact of Lifestyle": "Growing awareness of sunscreen and vitamin D supplementation."
    }
    # More countries can follow this format to complete the list of 50.
})

country_adaptations.update({

    "Chile": {
        "Adaptation Mechanisms": "Varied pigmentation due to high altitudes in the Andes and lower UV areas in the south.",
        "Historical Context": "Andean populations developed darker skin for UV protection at higher altitudes.",
        "Modern Challenges": "Urbanization and indoor lifestyles increase vitamin D deficiency risk.",
        "Exceptions": "Coastal populations receive less UV exposure and have lighter skin tones.",
        "Impact of Lifestyle": "Increasing public health awareness on vitamin D and sun exposure."
    },
    "United States": {
        "Adaptation Mechanisms": "Wide range of skin pigmentation due to diverse ancestry and varying UV exposure by region.",
        "Historical Context": "Lighter skin tones in northern regions, darker in the southern regions, adapted over time.",
        "Modern Challenges": "Indoor lifestyles contribute to vitamin D deficiency, especially in winter months.",
        "Exceptions": "Health disparities based on skin pigmentation in relation to UV exposure.",
        "Impact of Lifestyle": "Sunscreen use is highly encouraged, along with vitamin D supplements in northern regions."
    },
    "New Zealand": {
        "Adaptation Mechanisms": "Lighter skin tones among European-descended populations; indigenous Maori have darker skin.",
        "Historical Context": "Skin adaptations suited to high UV levels in the southern hemisphere.",
        "Modern Challenges": "High rates of skin cancer due to high UV exposure and light skin tones.",
        "Exceptions": "Maori populations have higher melanin levels, reducing skin cancer risk.",
        "Impact of Lifestyle": "Strong emphasis on sun safety, especially during peak UV times."
    },
    "Nepal": {
        "Adaptation Mechanisms": "Higher melanin levels among high-altitude populations for protection against strong UV radiation.",
        "Historical Context": "Darker pigmentation evolved in Himalayan regions to protect against intense UV at altitude.",
        "Modern Challenges": "Vitamin D deficiency is common in urban areas with limited outdoor exposure.",
        "Exceptions": "Lowland populations have lighter pigmentation and face more UV risks.",
        "Impact of Lifestyle": "Increasing awareness of vitamin D importance and sunscreen use."
    },
    "Poland": {
        "Adaptation Mechanisms": "Lower melanin levels to maximize vitamin D synthesis in low UV areas.",
        "Historical Context": "Lighter skin tones evolved due to limited sunlight in northern Europe.",
        "Modern Challenges": "Vitamin D deficiency is a widespread issue, especially in winter.",
        "Exceptions": "Immigrants from higher UV regions may face higher vitamin D deficiency risks.",
        "Impact of Lifestyle": "Vitamin D supplements and fortified foods are common in colder months."
    },
    "South Sudan": {
        "Adaptation Mechanisms": "High melanin levels as natural protection from intense equatorial sun.",
        "Historical Context": "Dark pigmentation evolved to protect against strong UV radiation year-round.",
        "Modern Challenges": "Vitamin D deficiency is less common due to regular outdoor activity.",
        "Exceptions": "Migrants to lower UV areas may face vitamin D synthesis challenges.",
        "Impact of Lifestyle": "Cultural emphasis on outdoor activities supports natural vitamin D production."
    },
    "Ethiopia": {
        "Adaptation Mechanisms": "High melanin levels in indigenous populations suited for equatorial sun exposure.",
        "Historical Context": "Dark pigmentation evolved to provide natural UV protection.",
        "Modern Challenges": "Vitamin D deficiency is not a significant issue due to high natural sunlight exposure.",
        "Exceptions": "Some urbanized areas see reduced sunlight exposure, impacting vitamin D levels.",
        "Impact of Lifestyle": "Public health campaigns encourage balanced sun exposure."
    },
    "Malaysia": {
        "Adaptation Mechanisms": "Higher melanin levels protect against intense tropical sun.",
        "Historical Context": "Dark skin pigmentation adapted to consistently high UV exposure.",
        "Modern Challenges": "Urbanization limits outdoor UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Rural populations receive more natural UV exposure.",
        "Impact of Lifestyle": "Increased focus on vitamin D awareness in urban centers."
    },
    "Finland": {
        "Adaptation Mechanisms": "Low melanin levels maximize vitamin D synthesis during low-sun months.",
        "Historical Context": "Lighter skin tones evolved in response to limited sunlight in northern latitudes.",
        "Modern Challenges": "Seasonal vitamin D deficiency is common during long winters.",
        "Exceptions": "Immigrant populations from high UV areas may face higher vitamin D deficiency risks.",
        "Impact of Lifestyle": "Widespread use of vitamin D supplements in winter."
    },
    "Ukraine": {
        "Adaptation Mechanisms": "Lower melanin levels help synthesize vitamin D in low UV areas.",
        "Historical Context": "Lighter skin tones developed in response to limited sunlight.",
        "Modern Challenges": "Vitamin D deficiency is common, especially in urban and northern populations.",
        "Exceptions": "Some southern regions see higher UV exposure, impacting skin pigmentation variation.",
        "Impact of Lifestyle": "Increased use of vitamin D supplements and awareness."
    },
    "Uganda": {
        "Adaptation Mechanisms": "High melanin levels provide protection from strong equatorial UV.",
        "Historical Context": "Dark pigmentation evolved due to consistent, intense sun exposure year-round.",
        "Modern Challenges": "Migration to lower UV regions brings adaptation challenges for vitamin D.",
        "Exceptions": "Albinism populations face significant health risks due to low melanin.",
        "Impact of Lifestyle": "Public health campaigns emphasize sunscreen and protective clothing."
    },
    "Ireland": {
        "Adaptation Mechanisms": "Very low melanin levels maximize vitamin D synthesis in a low UV environment.",
        "Historical Context": "Lighter skin tones adapted to frequent cloud cover and low sunlight.",
        "Modern Challenges": "Vitamin D deficiency is common, especially in winter.",
        "Exceptions": "Recent immigrants from high UV regions face increased vitamin D deficiency risks.",
        "Impact of Lifestyle": "Widespread use of vitamin D supplements, especially in winter."
    },
    "Iraq": {
        "Adaptation Mechanisms": "Moderate to dark pigmentation for protection against desert UV exposure.",
        "Historical Context": "Populations adapted to high levels of sun exposure in desert regions.",
        "Modern Challenges": "Urbanization and clothing habits limit UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Urban populations are particularly at risk for vitamin D deficiency.",
        "Impact of Lifestyle": "Increased public health focus on vitamin D supplementation and sun exposure."
    },
    "Sri Lanka": {
        "Adaptation Mechanisms": "High melanin levels in native populations to cope with tropical UV radiation.",
        "Historical Context": "Darker pigmentation evolved as a natural defense against intense sun.",
        "Modern Challenges": "Urban lifestyles reduce natural sunlight exposure, leading to vitamin D deficiency.",
        "Exceptions": "Some coastal populations receive higher sun exposure.",
        "Impact of Lifestyle": "Growing emphasis on vitamin D awareness and sunscreen use."
    },
    "Denmark": {
        "Adaptation Mechanisms": "Lower melanin levels to allow for maximum vitamin D synthesis in low UV regions.",
        "Historical Context": "Lighter skin evolved due to limited sunlight exposure.",
        "Modern Challenges": "Vitamin D deficiency is prevalent, especially in winter.",
        "Exceptions": "Recent immigrants from high UV regions have higher risks of vitamin D deficiency.",
        "Impact of Lifestyle": "Vitamin D supplementation and fortified foods are widely used."
    },
    "Mongolia": {
        "Adaptation Mechanisms": "Lower melanin levels to allow vitamin D synthesis in low UV conditions.",
        "Historical Context": "Lighter skin tones evolved due to long winters and low UV exposure.",
        "Modern Challenges": "Vitamin D deficiency is a significant concern, especially in winter months.",
        "Exceptions": "Rural, nomadic populations have higher natural UV exposure.",
        "Impact of Lifestyle": "Increased use of vitamin D supplements in urban areas."
    },
    "Venezuela": {
        "Adaptation Mechanisms": "Varied pigmentation based on tropical and mountainous regions.",
        "Historical Context": "Adapted to high UV levels in lowland areas and moderate UV in mountain regions.",
        "Modern Challenges": "Vitamin D deficiency growing in urban areas with limited sunlight.",
        "Exceptions": "High-altitude populations experience intense UV exposure.",
        "Impact of Lifestyle": "Awareness of vitamin D importance is increasing in urban areas."
    },
    "Cambodia": {
        "Adaptation Mechanisms": "Higher melanin levels for UV protection in a tropical climate.",
        "Historical Context": "Dark pigmentation evolved to protect against strong sunlight.",
        "Modern Challenges": "Urban migration reduces natural UV exposure, impacting vitamin D levels.",
        "Exceptions": "Rural areas see more natural sunlight exposure.",
        "Impact of Lifestyle": "Public health campaigns emphasize balanced UV exposure."
    },
    "Israel": {
        "Adaptation Mechanisms": "Moderate melanin levels adapted to high Mediterranean sun exposure.",
        "Historical Context": "Ancient populations adapted to high UV exposure and intense sunlight.",
        "Modern Challenges": "High UV exposure leads to increased skin cancer risks among light-skinned populations.",
        "Exceptions": "Immigrant populations with varied pigmentation may experience different health risks.",
        "Impact of Lifestyle": "Sunscreen usage and sun safety awareness are widespread."
    },
    "Romania": {
        "Adaptation Mechanisms": "Lighter skin tones evolved to enable vitamin D synthesis in low UV conditions.",
        "Historical Context": "Populations adapted to limited sunlight, particularly in winter months.",
        "Modern Challenges": "Vitamin D deficiency is common, especially during long winters.",
        "Exceptions": "Immigrants from regions with high UV exposure face additional vitamin D challenges.",
        "Impact of Lifestyle": "Increased awareness on vitamin D supplements, especially in urban areas."
    }
})

country_adaptations.update({
    "Afghanistan": {
        "Adaptation Mechanisms": "Moderate to dark skin tones in southern and lowland regions; lighter skin tones in mountainous areas.",
        "Historical Context": "Adaptations to intense UV exposure in desert and mountainous regions.",
        "Modern Challenges": "Vitamin D deficiency is common in urban populations with limited outdoor activities.",
        "Exceptions": "Mountain populations face different UV exposure levels compared to lowlands.",
        "Impact of Lifestyle": "Increased use of vitamin D supplements, especially in cities."
    },
    "Ghana": {
        "Adaptation Mechanisms": "High melanin levels in native populations to provide natural protection against intense UV.",
        "Historical Context": "Dark skin pigmentation evolved as a defense against high UV levels in tropical environments.",
        "Modern Challenges": "Shift to urban environments with less outdoor activity can lead to vitamin D deficiency.",
        "Exceptions": "People with albinism are particularly vulnerable to UV-related health issues.",
        "Impact of Lifestyle": "Education on sunscreen and vitamin D awareness is increasing in urban areas."
    },
    "Morocco": {
        "Adaptation Mechanisms": "Darker skin tones in desert regions provide UV protection; lighter tones in coastal areas.",
        "Historical Context": "Adapted to varying UV levels, from coastal to desert regions.",
        "Modern Challenges": "Urban migration has led to reduced UV exposure and potential vitamin D deficiency.",
        "Exceptions": "Fair-skinned populations in northern areas face increased UV risks.",
        "Impact of Lifestyle": "Public health campaigns focus on balanced sun exposure and vitamin D."
    },
    "Switzerland": {
        "Adaptation Mechanisms": "Lighter skin tones to maximize vitamin D synthesis in low UV regions.",
        "Historical Context": "Evolved lighter skin due to high altitude and limited sunlight.",
        "Modern Challenges": "Vitamin D deficiency, especially in winter months.",
        "Exceptions": "Some immigrant populations may have different vitamin D needs.",
        "Impact of Lifestyle": "Vitamin D supplementation is common, especially in winter."
    },
    "Gambia": {
        "Adaptation Mechanisms": "High melanin levels adapted to high UV exposure in tropical climates.",
        "Historical Context": "Darker pigmentation evolved for UV protection in equatorial regions.",
        "Modern Challenges": "Urbanization and less outdoor activity can lead to vitamin D deficiency.",
        "Exceptions": "People with albinism face significant UV-related health risks.",
        "Impact of Lifestyle": "Education on sun safety and vitamin D is increasing in urban areas."
    },
    "Zimbabwe": {
        "Adaptation Mechanisms": "Higher melanin levels provide protection against strong UV in tropical and highland regions.",
        "Historical Context": "Adapted to intense sunlight exposure, particularly in the highlands.",
        "Modern Challenges": "Vitamin D deficiency in urban settings due to indoor lifestyles.",
        "Exceptions": "Rural populations tend to have greater natural UV exposure.",
        "Impact of Lifestyle": "Public health focus on vitamin D awareness and sun safety."
    },
    "Libya": {
        "Adaptation Mechanisms": "Darker skin tones provide protection against intense desert UV radiation.",
        "Historical Context": "Adapted to high UV levels in desert regions.",
        "Modern Challenges": "Urban lifestyles reduce natural UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Lighter-skinned populations have higher UV vulnerability.",
        "Impact of Lifestyle": "Increased vitamin D supplementation and sun protection campaigns."
    },
    "Lebanon": {
        "Adaptation Mechanisms": "Moderate pigmentation suited to Mediterranean UV exposure.",
        "Historical Context": "Mixed ancestry led to a variety of skin tones across the population.",
        "Modern Challenges": "Vitamin D deficiency is growing, especially in urban settings.",
        "Exceptions": "Northern regions see higher UV exposure compared to the south.",
        "Impact of Lifestyle": "Awareness of sunscreen and vitamin D is increasing."
    },
    "Jordan": {
        "Adaptation Mechanisms": "Darker skin tones in desert regions adapted to intense sunlight.",
        "Historical Context": "Evolved pigmentation suitable for a high UV desert environment.",
        "Modern Challenges": "Vitamin D deficiency due to limited sun exposure and indoor work.",
        "Exceptions": "Urban populations face greater risk of vitamin D deficiency.",
        "Impact of Lifestyle": "Public health campaigns on vitamin D supplementation and sun safety."
    },
    "Bolivia": {
        "Adaptation Mechanisms": "High melanin levels provide protection at high altitudes where UV is intense.",
        "Historical Context": "Dark skin pigmentation in Andean populations adapted to high-altitude UV exposure.",
        "Modern Challenges": "Vitamin D deficiency is an increasing issue in urban areas.",
        "Exceptions": "Lowland populations face lower UV exposure than those in high-altitude regions.",
        "Impact of Lifestyle": "Awareness of vitamin D and UV safety is increasing."
    },
    "Honduras": {
        "Adaptation Mechanisms": "Darker skin tones adapted to intense UV exposure in tropical environments.",
        "Historical Context": "Adaptations to high humidity and UV levels along the coasts and jungles.",
        "Modern Challenges": "Urban migration reduces natural UV exposure and vitamin D levels.",
        "Exceptions": "Coastal populations are more exposed to natural sunlight than urban areas.",
        "Impact of Lifestyle": "Growing awareness of vitamin D deficiency and UV protection."
    },
    "Serbia": {
        "Adaptation Mechanisms": "Lighter skin tones in response to low UV exposure in temperate regions.",
        "Historical Context": "Evolved lighter skin to maximize vitamin D synthesis in low UV areas.",
        "Modern Challenges": "Vitamin D deficiency, particularly in urban populations and during winter.",
        "Exceptions": "Immigrant populations may have higher risks of vitamin D deficiency.",
        "Impact of Lifestyle": "Vitamin D supplements and sun exposure awareness are increasing."
    },
    "Portugal": {
        "Adaptation Mechanisms": "Moderate pigmentation levels adapted to Mediterranean UV exposure.",
        "Historical Context": "Adapted to a sunny, coastal climate with a mix of lighter and darker skin tones.",
        "Modern Challenges": "Increased skin cancer rates among fair-skinned populations.",
        "Exceptions": "Southern regions may have slightly darker pigmentation than the north.",
        "Impact of Lifestyle": "Public health initiatives focus on sun protection and vitamin D awareness."
    },
    "Madagascar": {
        "Adaptation Mechanisms": "Higher melanin levels provide UV protection in tropical and highland areas.",
        "Historical Context": "Adaptations to intense sunlight and varied UV exposure across the island.",
        "Modern Challenges": "Vitamin D deficiency concerns in urban and high-altitude areas.",
        "Exceptions": "Coastal populations experience more intense sunlight.",
        "Impact of Lifestyle": "Increased awareness of vitamin D and sun protection."
    },
    "Armenia": {
        "Adaptation Mechanisms": "Lighter skin tones to synthesize vitamin D in mountainous, low UV regions.",
        "Historical Context": "Populations adapted to low UV exposure, especially in high-altitude areas.",
        "Modern Challenges": "Vitamin D deficiency is common, especially in winter.",
        "Exceptions": "Urbanization has led to decreased outdoor UV exposure.",
        "Impact of Lifestyle": "Growing use of vitamin D supplements and sun exposure awareness."
    },
    "Sudan": {
        "Adaptation Mechanisms": "High melanin levels adapted to intense UV exposure in desert regions.",
        "Historical Context": "Dark pigmentation provides natural UV protection for desert populations.",
        "Modern Challenges": "Vitamin D deficiency concerns in urbanized populations with less sun exposure.",
        "Exceptions": "People with albinism face significant risks due to low melanin protection.",
        "Impact of Lifestyle": "Education on sunscreen and vitamin D is increasing in urban areas."
    },
    "Hungary": {
        "Adaptation Mechanisms": "Lighter skin tones evolved in response to low UV exposure in temperate regions.",
        "Historical Context": "Adapted to low UV radiation with skin tones suited for vitamin D synthesis.",
        "Modern Challenges": "Vitamin D deficiency, especially during the winter months.",
        "Exceptions": "Immigrants from higher UV regions face increased vitamin D risks.",
        "Impact of Lifestyle": "Widespread use of vitamin D supplements and sun exposure awareness."
    },
    "Tanzania": {
        "Adaptation Mechanisms": "Higher melanin levels provide UV protection in equatorial and highland areas.",
        "Historical Context": "Dark skin pigmentation evolved to shield from strong UV exposure year-round.",
        "Modern Challenges": "Urbanization decreases natural sunlight exposure, impacting vitamin D.",
        "Exceptions": "Albinism is prevalent, leading to increased UV-related health risks.",
        "Impact of Lifestyle": "Public health campaigns focus on sunscreen and vitamin D education."
    },
    "Tunisia": {
        "Adaptation Mechanisms": "Darker skin tones provide protection against Mediterranean and desert UV levels.",
        "Historical Context": "Adapted to high UV radiation in both coastal and desert environments.",
        "Modern Challenges": "Urban migration reduces natural UV exposure, leading to vitamin D issues.",
        "Exceptions": "Fair-skinned populations face higher UV risks.",
        "Impact of Lifestyle": "Public awareness on sunscreen and vitamin D is increasing."
    },
    "Netherlands": {
        "Adaptation Mechanisms": "Very light skin tones to maximize vitamin D synthesis in low UV areas.",
        "Historical Context": "Adapted to low sunlight levels with low melanin levels for vitamin D production.",
        "Modern Challenges": "Vitamin D deficiency is common in the winter months.",
        "Exceptions": "Immigrant populations from high UV regions face higher deficiency risks.",
        "Impact of Lifestyle": "Widespread vitamin D supplementation and public health awareness."
    },
    "Belgium": {
        "Adaptation Mechanisms": "Light skin tones help synthesize vitamin D in low UV conditions.",
        "Historical Context": "Lighter skin evolved due to limited sunlight in northern Europe.",
        "Modern Challenges": "Vitamin D deficiency is prevalent, especially in winter.",
        "Exceptions": "Immigrants from high UV regions face higher deficiency risks.",
        "Impact of Lifestyle": "Increased use of vitamin D supplements and fortified foods."
    }
})

country_adaptations.update({
    "Vietnam": {
        "Adaptation Mechanisms": "Higher melanin levels provide UV protection in a tropical climate.",
        "Historical Context": "Adaptations to consistent UV exposure, with darker skin tones in southern regions.",
        "Modern Challenges": "Urban lifestyles reduce natural sunlight exposure, leading to potential vitamin D deficiency.",
        "Exceptions": "Rural populations still receive more natural sunlight than urban areas.",
        "Impact of Lifestyle": "Increasing focus on vitamin D supplementation and sun safety in urban centers."
    },
    "Greece": {
        "Adaptation Mechanisms": "Moderate melanin levels suited to Mediterranean climate and UV exposure.",
        "Historical Context": "Populations adapted to sunny, coastal UV levels with varied skin tones.",
        "Modern Challenges": "Rising skin cancer rates due to prolonged summer sun exposure.",
        "Exceptions": "Lighter-skinned populations in northern Greece face greater UV risks.",
        "Impact of Lifestyle": "High sunscreen use and awareness campaigns, especially in coastal areas."
    },
    "Austria": {
        "Adaptation Mechanisms": "Lighter skin tones enable vitamin D synthesis in lower UV environments.",
        "Historical Context": "Adapted to moderate sunlight exposure in mountainous and temperate regions.",
        "Modern Challenges": "Vitamin D deficiency, especially in the winter months.",
        "Exceptions": "Immigrant populations from high UV regions may have higher deficiency risks.",
        "Impact of Lifestyle": "Common use of vitamin D supplements and increased awareness of sun exposure."
    },
    "Czech Republic": {
        "Adaptation Mechanisms": "Lower melanin levels to maximize vitamin D synthesis in low UV conditions.",
        "Historical Context": "Adapted to limited UV exposure in central European climate.",
        "Modern Challenges": "Vitamin D deficiency is widespread, especially in winter months.",
        "Exceptions": "Some immigrant populations face unique vitamin D requirements.",
        "Impact of Lifestyle": "Vitamin D supplements and fortified foods are increasingly common."
    },
    "Ecuador": {
        "Adaptation Mechanisms": "Higher melanin levels for UV protection in equatorial and high-altitude regions.",
        "Historical Context": "Populations in the Andes adapted to intense UV exposure at altitude.",
        "Modern Challenges": "Vitamin D deficiency in urban populations with reduced sunlight exposure.",
        "Exceptions": "Lower-altitude populations experience less intense UV.",
        "Impact of Lifestyle": "Vitamin D awareness is growing in urban areas and high-altitude regions."
    },
    "Rwanda": {
        "Adaptation Mechanisms": "High melanin levels adapted to equatorial UV radiation.",
        "Historical Context": "Dark pigmentation evolved to protect against consistent, intense sunlight.",
        "Modern Challenges": "Vitamin D deficiency concerns in urbanized populations with less sun exposure.",
        "Exceptions": "Rural populations receive consistent natural sunlight, reducing deficiency risks.",
        "Impact of Lifestyle": "Public health initiatives focus on balanced sun exposure and vitamin D awareness."
    },
    "Sweden": {
        "Adaptation Mechanisms": "Very light skin tones maximize vitamin D synthesis in low UV conditions.",
        "Historical Context": "Adapted to long winters and low sunlight, resulting in low melanin levels.",
        "Modern Challenges": "Vitamin D deficiency is widespread, especially during winter.",
        "Exceptions": "Immigrants from high UV areas may have unique vitamin D needs.",
        "Impact of Lifestyle": "Widespread use of vitamin D supplements during winter."
    },
    "Ireland": {
        "Adaptation Mechanisms": "Very light skin tones to allow for maximum vitamin D synthesis in low UV conditions.",
        "Historical Context": "Adapted to frequent cloud cover and limited sunlight exposure.",
        "Modern Challenges": "Vitamin D deficiency is common, especially during winter months.",
        "Exceptions": "Immigrants from high UV regions face greater risks of vitamin D deficiency.",
        "Impact of Lifestyle": "Vitamin D supplements and fortified foods are increasingly common."
    },
    "Jamaica": {
        "Adaptation Mechanisms": "Higher melanin levels in indigenous populations protect against high tropical UV.",
        "Historical Context": "Dark pigmentation adapted to consistently high UV levels near the equator.",
        "Modern Challenges": "Migration to lower UV regions or indoor work can lead to vitamin D deficiency.",
        "Exceptions": "People with albinism face significant health risks due to low melanin protection.",
        "Impact of Lifestyle": "Public awareness of sunscreen and vitamin D supplementation is increasing."
    },
    "Portugal": {
        "Adaptation Mechanisms": "Moderate pigmentation levels suitable for Mediterranean climate.",
        "Historical Context": "Adapted to varying UV exposure along the coastal and mountainous regions.",
        "Modern Challenges": "Increased skin cancer risk for fair-skinned populations in the south.",
        "Exceptions": "Southern regions generally experience higher UV exposure.",
        "Impact of Lifestyle": "Sunscreen use is common, with public health campaigns on sun safety."
    },
    "Iran": {
        "Adaptation Mechanisms": "Moderate to dark skin tones, especially in desert and highland regions.",
        "Historical Context": "Populations adapted to UV exposure in a mix of desert and mountainous regions.",
        "Modern Challenges": "Urban lifestyles reduce natural UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Mountain populations experience varying UV exposure.",
        "Impact of Lifestyle": "Vitamin D supplements and sun safety awareness are on the rise."
    },
    "Belgium": {
        "Adaptation Mechanisms": "Light skin tones maximize vitamin D synthesis in low UV conditions.",
        "Historical Context": "Populations adapted to limited sunlight, particularly during winter.",
        "Modern Challenges": "Vitamin D deficiency is common, especially during the colder months.",
        "Exceptions": "Immigrant populations from high UV regions may face unique vitamin D needs.",
        "Impact of Lifestyle": "Vitamin D supplements and fortified foods are widely available."
    },
    "Algeria": {
        "Adaptation Mechanisms": "Darker skin tones adapted to intense desert UV radiation.",
        "Historical Context": "Adaptations to harsh, sunny conditions in desert and coastal areas.",
        "Modern Challenges": "Urbanization has led to reduced natural UV exposure and vitamin D deficiency.",
        "Exceptions": "Lighter-skinned populations face higher UV risks.",
        "Impact of Lifestyle": "Public health campaigns promote vitamin D supplementation and sun safety."
    },
    "South Korea": {
        "Adaptation Mechanisms": "Moderate pigmentation adapted to seasonal changes in UV exposure.",
        "Historical Context": "Skin tones adapted to a temperate climate with varied seasonal UV.",
        "Modern Challenges": "Vitamin D deficiency due to indoor lifestyles and pollution.",
        "Exceptions": "Higher skin cancer rates among fair-skinned individuals.",
        "Impact of Lifestyle": "Vitamin D supplements are common, along with awareness of sun protection."
    },
    "Italy": {
        "Adaptation Mechanisms": "Varied pigmentation from darker skin in southern Italy to lighter skin in the north.",
        "Historical Context": "Adaptations to varying UV exposure across different Italian regions.",
        "Modern Challenges": "Higher skin cancer rates among lighter-skinned populations in northern Italy.",
        "Exceptions": "Darker skin tones in southern Italy adapted to higher UV levels.",
        "Impact of Lifestyle": "Sunscreen and sun-protection campaigns are common, especially in summer."
    },
    "Finland": {
        "Adaptation Mechanisms": "Very light skin tones evolved to maximize vitamin D synthesis in low-sun conditions.",
        "Historical Context": "Long winters and limited sunlight led to low melanin levels.",
        "Modern Challenges": "Vitamin D deficiency is common, especially in winter months.",
        "Exceptions": "Recent immigrant populations may face unique vitamin D needs.",
        "Impact of Lifestyle": "Vitamin D supplementation is widespread, particularly during winter."
    },
    "Colombia": {
        "Adaptation Mechanisms": "Diverse pigmentation adapted to tropical, mountainous, and coastal UV levels.",
        "Historical Context": "Higher UV regions influenced darker pigmentation in coastal and highland areas.",
        "Modern Challenges": "Urban migration leads to lower sunlight exposure, resulting in vitamin D issues.",
        "Exceptions": "Mountain populations adapted to high UV exposure at altitude.",
        "Impact of Lifestyle": "Vitamin D awareness is increasing in urban areas, along with sun safety education."
    },
    "Argentina": {
        "Adaptation Mechanisms": "Varied pigmentation, with darker skin tones in the north and lighter in the south.",
        "Historical Context": "Adapted to a range of UV levels from tropical north to temperate south.",
        "Modern Challenges": "Vitamin D deficiency is common in urban areas due to indoor lifestyles.",
        "Exceptions": "Fair-skinned European-descendant populations face higher UV risks.",
        "Impact of Lifestyle": "Public health efforts focus on sunscreen and vitamin D awareness."
    },
    "Cuba": {
        "Adaptation Mechanisms": "Higher melanin levels suited to tropical UV exposure.",
        "Historical Context": "Adaptations to consistent UV radiation in a tropical climate.",
        "Modern Challenges": "Urbanization and indoor lifestyles reduce natural sunlight exposure.",
        "Exceptions": "Coastal populations receive greater natural UV exposure.",
        "Impact of Lifestyle": "Sunscreen use is encouraged, along with awareness on vitamin D."
    },
    "El Salvador": {
        "Adaptation Mechanisms": "Higher melanin levels adapted to high UV exposure in tropical areas.",
        "Historical Context": "Populations developed dark skin to protect against intense UV.",
        "Modern Challenges": "Urban lifestyles reduce natural UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Rural populations are still exposed to consistent natural sunlight.",
        "Impact of Lifestyle": "Awareness of vitamin D and sun safety is increasing, especially in cities."
    },
    "Nigeria": {
        "Adaptation Mechanisms": "High melanin levels provide natural protection against intense UV in tropical climates.",
        "Historical Context": "Dark skin pigmentation evolved to protect against high UV exposure near the equator.",
        "Modern Challenges": "Urban migration leads to vitamin D deficiency due to reduced outdoor activities.",
        "Exceptions": "People with albinism face significant UV-related health risks.",
        "Impact of Lifestyle": "Growing awareness of sunscreen and vitamin D, especially in urban areas."
    }
})

country_adaptations.update({
    "Poland": {
        "Adaptation Mechanisms": "Light skin tones maximize vitamin D synthesis in lower UV conditions.",
        "Historical Context": "Adapted to limited sunlight exposure, especially during long winters.",
        "Modern Challenges": "Vitamin D deficiency is prevalent due to low natural sunlight in winter.",
        "Exceptions": "Immigrants from higher UV regions may face greater vitamin D deficiency risks.",
        "Impact of Lifestyle": "Vitamin D supplementation is common, especially in winter months."
    },
    "Czech Republic": {
        "Adaptation Mechanisms": "Lower melanin levels help in vitamin D synthesis under low UV conditions.",
        "Historical Context": "Adapted to moderate UV exposure with lighter skin tones.",
        "Modern Challenges": "Vitamin D deficiency is common in winter due to limited sunlight exposure.",
        "Exceptions": "Recent immigrants from high UV regions may require additional vitamin D.",
        "Impact of Lifestyle": "Public health initiatives emphasize vitamin D supplements, especially in winter."
    },
    "Hungary": {
        "Adaptation Mechanisms": "Lighter skin tones maximize vitamin D synthesis in a temperate climate.",
        "Historical Context": "Adapted to moderate UV levels in the central European climate.",
        "Modern Challenges": "Vitamin D deficiency is prevalent, particularly in urban and northern populations.",
        "Exceptions": "Immigrants from higher UV regions may require higher vitamin D intake.",
        "Impact of Lifestyle": "Widespread use of vitamin D supplements during winter months."
    },
    "Romania": {
        "Adaptation Mechanisms": "Lighter skin tones developed to allow for vitamin D synthesis in low UV conditions.",
        "Historical Context": "Adapted to a range of UV exposure across the country, with mountainous and lowland areas.",
        "Modern Challenges": "Vitamin D deficiency, especially in urban and winter months.",
        "Exceptions": "People in mountainous regions experience higher UV exposure compared to lowlands.",
        "Impact of Lifestyle": "Vitamin D supplements are common, with public health campaigns on sun exposure."
    },
    "Ukraine": {
        "Adaptation Mechanisms": "Lighter skin tones evolved to maximize vitamin D synthesis in low UV regions.",
        "Historical Context": "Adapted to low sunlight exposure, especially during long, cold winters.",
        "Modern Challenges": "Vitamin D deficiency is common, particularly in northern regions and urban areas.",
        "Exceptions": "Southern populations may experience slightly more UV exposure.",
        "Impact of Lifestyle": "Increasing use of vitamin D supplements and fortified foods in colder months."
    },
    "Belarus": {
        "Adaptation Mechanisms": "Very light skin tones allow for vitamin D synthesis in low UV conditions.",
        "Historical Context": "Adapted to low sunlight exposure with minimal melanin levels.",
        "Modern Challenges": "Vitamin D deficiency is common, especially during the winter season.",
        "Exceptions": "Immigrant populations may require additional vitamin D intake.",
        "Impact of Lifestyle": "Vitamin D supplementation is widespread in winter, with growing public health awareness."
    },
    "Estonia": {
        "Adaptation Mechanisms": "Light skin tones maximize vitamin D synthesis in low UV environments.",
        "Historical Context": "Adapted to long winters and minimal sunlight with low melanin levels.",
        "Modern Challenges": "Vitamin D deficiency is prevalent during extended winter months.",
        "Exceptions": "Immigrants from higher UV areas may face unique vitamin D requirements.",
        "Impact of Lifestyle": "Widespread vitamin D supplementation, especially during winter."
    },
    "Latvia": {
        "Adaptation Mechanisms": "Very light skin tones enable vitamin D synthesis in low UV conditions.",
        "Historical Context": "Adapted to low sunlight exposure and long winters with minimal melanin levels.",
        "Modern Challenges": "Vitamin D deficiency is common in winter due to low natural UV exposure.",
        "Exceptions": "Recent immigrants from higher UV areas may have unique vitamin D needs.",
        "Impact of Lifestyle": "Vitamin D supplements and fortified foods are commonly used in winter."
    },
    "Lithuania": {
        "Adaptation Mechanisms": "Low melanin levels maximize vitamin D synthesis in low UV regions.",
        "Historical Context": "Adapted to long winters and minimal sunlight with very light skin tones.",
        "Modern Challenges": "Vitamin D deficiency is common, especially in colder months.",
        "Exceptions": "Immigrants from higher UV regions may require additional vitamin D.",
        "Impact of Lifestyle": "Public health campaigns focus on vitamin D supplements, especially in winter."
    },
    "Slovakia": {
        "Adaptation Mechanisms": "Lighter skin tones help in vitamin D synthesis in moderate UV conditions.",
        "Historical Context": "Populations adapted to a temperate, mountainous climate with varied UV exposure.",
        "Modern Challenges": "Vitamin D deficiency is common in winter and among urban populations.",
        "Exceptions": "Mountain populations may receive higher UV exposure than lowland areas.",
        "Impact of Lifestyle": "Increasing use of vitamin D supplements and public health awareness on sun exposure."
    },
    "Bulgaria": {
        "Adaptation Mechanisms": "Lighter skin tones adapted to temperate climate with seasonal UV changes.",
        "Historical Context": "Adapted to moderate UV exposure with a range of skin tones across the country.",
        "Modern Challenges": "Vitamin D deficiency in winter and among urban populations.",
        "Exceptions": "Southern populations may have slightly higher UV exposure than northern ones.",
        "Impact of Lifestyle": "Increased use of vitamin D supplements and awareness on sun safety."
    },
    "Croatia": {
        "Adaptation Mechanisms": "Lighter skin tones in northern regions; moderate pigmentation in coastal areas.",
        "Historical Context": "Adapted to varied UV exposure from coastal to inland regions.",
        "Modern Challenges": "Vitamin D deficiency, especially in winter and urban populations.",
        "Exceptions": "Darker skin tones are more common in southern, Mediterranean regions.",
        "Impact of Lifestyle": "Public health campaigns on vitamin D supplementation and sun exposure are common."
    },
    "Serbia": {
        "Adaptation Mechanisms": "Lighter skin tones maximize vitamin D synthesis in temperate climates.",
        "Historical Context": "Adapted to moderate UV exposure in the central Balkans.",
        "Modern Challenges": "Vitamin D deficiency is common, particularly in winter months.",
        "Exceptions": "Immigrant populations from higher UV areas may face unique vitamin D needs.",
        "Impact of Lifestyle": "Vitamin D supplements are increasingly common, with public health awareness rising."
    },
    "Slovenia": {
        "Adaptation Mechanisms": "Lighter skin tones in response to low UV exposure in temperate and mountainous areas.",
        "Historical Context": "Adapted to low sunlight with skin tones suited for vitamin D synthesis.",
        "Modern Challenges": "Vitamin D deficiency is common, particularly in winter.",
        "Exceptions": "Immigrants from high UV regions may face unique vitamin D needs.",
        "Impact of Lifestyle": "Increasing use of vitamin D supplements and public health campaigns on sun exposure."
    },
    "Bosnia and Herzegovina": {
        "Adaptation Mechanisms": "Lighter skin tones evolved in response to moderate UV exposure in a temperate climate.",
        "Historical Context": "Adapted to moderate sunlight levels in mountainous and lowland regions.",
        "Modern Challenges": "Vitamin D deficiency is common in winter and among urban populations.",
        "Exceptions": "Immigrant populations from higher UV areas may face unique vitamin D needs.",
        "Impact of Lifestyle": "Vitamin D supplements are increasingly common, with growing public health awareness."
    },
    "Moldova": {
        "Adaptation Mechanisms": "Lighter skin tones evolved in response to low UV exposure in a temperate climate.",
        "Historical Context": "Adapted to moderate sunlight exposure, especially in winter.",
        "Modern Challenges": "Vitamin D deficiency is prevalent, especially in winter and urban areas.",
        "Exceptions": "Immigrant populations may face unique vitamin D needs.",
        "Impact of Lifestyle": "Public health campaigns on vitamin D supplementation and balanced sun exposure."
    },
    "Montenegro": {
        "Adaptation Mechanisms": "Varied pigmentation, with darker skin tones in coastal areas and lighter inland.",
        "Historical Context": "Adapted to varying UV levels from coastal Mediterranean to mountainous regions.",
        "Modern Challenges": "Vitamin D deficiency is common, especially in winter and urban areas.",
        "Exceptions": "Coastal populations receive more natural UV exposure than inland populations.",
        "Impact of Lifestyle": "Increased focus on vitamin D supplementation and sun protection awareness."
    },
    "Albania": {
        "Adaptation Mechanisms": "Moderate pigmentation suited to Mediterranean climate and UV exposure.",
        "Historical Context": "Adapted to moderate UV exposure, with darker skin tones in southern regions.",
        "Modern Challenges": "Vitamin D deficiency is rising, especially in winter and urban areas.",
        "Exceptions": "Northern populations with lighter skin tones face greater UV sensitivity.",
        "Impact of Lifestyle": "Public health campaigns encourage vitamin D supplements and sun protection."
    }
})

country_adaptations.update({
    "United Kingdom": {
        "Adaptation Mechanisms": "Very light skin tones to maximize vitamin D synthesis in low UV conditions.",
        "Historical Context": "Adapted to frequent cloud cover and limited sunlight exposure.",
        "Modern Challenges": "Vitamin D deficiency is common, particularly during winter months.",
        "Exceptions": "Immigrants from high UV regions face higher risks of vitamin D deficiency.",
        "Impact of Lifestyle": "Vitamin D supplements and fortified foods are commonly used, with public health campaigns promoting sun exposure."
    },
    "Ireland": {
        "Adaptation Mechanisms": "Very light skin tones evolved to allow for maximum vitamin D synthesis in low UV conditions.",
        "Historical Context": "Adapted to frequent cloud cover and minimal sunlight exposure.",
        "Modern Challenges": "Vitamin D deficiency is prevalent, especially during long winter months.",
        "Exceptions": "Immigrant populations may face unique vitamin D requirements.",
        "Impact of Lifestyle": "Widespread use of vitamin D supplements, especially in winter, with emphasis on balanced sun exposure."
    },
    "France": {
        "Adaptation Mechanisms": "Moderate pigmentation, with lighter skin tones in the north and slightly darker tones in the south.",
        "Historical Context": "Adapted to varied UV exposure across northern and southern regions.",
        "Modern Challenges": "Higher skin cancer rates among fair-skinned populations, especially in southern France.",
        "Exceptions": "Southern regions generally receive higher UV exposure, influencing skin tone variation.",
        "Impact of Lifestyle": "Public health campaigns focus on sun protection, especially in coastal and Mediterranean areas."
    },
    "Germany": {
        "Adaptation Mechanisms": "Light skin tones maximize vitamin D synthesis in low UV environments.",
        "Historical Context": "Adapted to limited sunlight and frequent cloud cover, particularly in northern Germany.",
        "Modern Challenges": "Vitamin D deficiency is common in winter due to low sunlight exposure.",
        "Exceptions": "Immigrant populations from high UV regions face greater risks of vitamin D deficiency.",
        "Impact of Lifestyle": "Widespread use of vitamin D supplements, with increasing awareness on balanced sun exposure."
    },
    "Netherlands": {
        "Adaptation Mechanisms": "Very light skin tones to maximize vitamin D synthesis in low UV conditions.",
        "Historical Context": "Adapted to frequent overcast skies and limited sunlight.",
        "Modern Challenges": "Vitamin D deficiency is prevalent, especially in winter months.",
        "Exceptions": "Immigrants from high UV regions may face greater risks of vitamin D deficiency.",
        "Impact of Lifestyle": "Vitamin D supplements and fortified foods are widely used, with increased awareness on sun exposure."
    },
    "Belgium": {
        "Adaptation Mechanisms": "Light skin tones help synthesize vitamin D in low UV environments.",
        "Historical Context": "Adapted to low sunlight exposure, especially in winter.",
        "Modern Challenges": "Vitamin D deficiency is common, particularly during colder months.",
        "Exceptions": "Immigrant populations from high UV regions may require additional vitamin D intake.",
        "Impact of Lifestyle": "Public health initiatives promote vitamin D supplements and balanced sun exposure."
    },
    "Switzerland": {
        "Adaptation Mechanisms": "Light skin tones maximize vitamin D synthesis in low UV conditions, especially at high altitudes.",
        "Historical Context": "Adapted to low sunlight, particularly during long winters in mountainous regions.",
        "Modern Challenges": "Vitamin D deficiency is prevalent, especially in northern regions and during winter.",
        "Exceptions": "Immigrant populations may have unique vitamin D needs.",
        "Impact of Lifestyle": "Widespread vitamin D supplementation, especially in winter months."
    },
    "Austria": {
        "Adaptation Mechanisms": "Lighter skin tones allow for vitamin D synthesis in a temperate, low UV climate.",
        "Historical Context": "Adapted to moderate sunlight levels, with long winters in mountainous areas.",
        "Modern Challenges": "Vitamin D deficiency is prevalent during the colder months.",
        "Exceptions": "Recent immigrants from high UV regions may require additional vitamin D.",
        "Impact of Lifestyle": "Vitamin D supplements and sun exposure awareness are common, especially in winter."
    },
    "Portugal": {
        "Adaptation Mechanisms": "Moderate pigmentation suited to Mediterranean climate and UV exposure.",
        "Historical Context": "Adapted to varied UV exposure, with lighter skin tones in the north and slightly darker in southern regions.",
        "Modern Challenges": "Increased skin cancer risk among fair-skinned populations in coastal areas.",
        "Exceptions": "Southern populations experience slightly more UV exposure than northern ones.",
        "Impact of Lifestyle": "Public health campaigns emphasize sun protection and vitamin D awareness."
    },
    "Spain": {
        "Adaptation Mechanisms": "Moderate pigmentation levels adapted to Mediterranean climate and UV exposure.",
        "Historical Context": "Adapted to varied UV exposure across northern and southern regions.",
        "Modern Challenges": "Higher skin cancer rates among fair-skinned populations in sunny regions.",
        "Exceptions": "Southern populations experience higher UV exposure, influencing skin tone variation.",
        "Impact of Lifestyle": "Sunscreen use is encouraged, particularly in high UV regions and during summer."
    },
    "Italy": {
        "Adaptation Mechanisms": "Varied pigmentation, with darker skin tones in southern Italy and lighter in the north.",
        "Historical Context": "Adapted to different UV exposure levels, from sunny Mediterranean regions to the cooler north.",
        "Modern Challenges": "Higher skin cancer risks among fair-skinned populations, especially in northern Italy.",
        "Exceptions": "Southern populations with darker skin tones are adapted to higher UV levels.",
        "Impact of Lifestyle": "Public health campaigns on sunscreen use and balanced vitamin D intake."
    },
    "Luxembourg": {
        "Adaptation Mechanisms": "Light skin tones maximize vitamin D synthesis in low UV conditions.",
        "Historical Context": "Adapted to limited sunlight exposure, particularly during colder months.",
        "Modern Challenges": "Vitamin D deficiency is common, especially during winter.",
        "Exceptions": "Immigrants from high UV regions face higher risks of vitamin D deficiency.",
        "Impact of Lifestyle": "Increasing use of vitamin D supplements and awareness of sun exposure."
    },
    "Monaco": {
        "Adaptation Mechanisms": "Moderate pigmentation adapted to Mediterranean climate with moderate UV exposure.",
        "Historical Context": "Adapted to sunny coastal regions with moderate skin tones.",
        "Modern Challenges": "Skin cancer rates are higher among fair-skinned populations.",
        "Exceptions": "Lighter-skinned individuals in northern regions face more UV-related health risks.",
        "Impact of Lifestyle": "Public health campaigns emphasize sun protection, especially in summer."
    },
    "Liechtenstein": {
        "Adaptation Mechanisms": "Light skin tones evolved to enable vitamin D synthesis in lower UV environments.",
        "Historical Context": "Adapted to low sunlight and mountainous conditions with very light skin tones.",
        "Modern Challenges": "Vitamin D deficiency is common, especially in winter months.",
        "Exceptions": "Immigrant populations may require additional vitamin D intake.",
        "Impact of Lifestyle": "Vitamin D supplements and fortified foods are commonly used in winter."
    },
    "Andorra": {
        "Adaptation Mechanisms": "Light skin tones evolved to maximize vitamin D synthesis in low sunlight conditions at high altitudes.",
        "Historical Context": "Adapted to low UV exposure in mountainous and temperate climates.",
        "Modern Challenges": "Vitamin D deficiency is prevalent, particularly during winter.",
        "Exceptions": "Immigrant populations from high UV areas may require additional vitamin D intake.",
        "Impact of Lifestyle": "Public health campaigns focus on vitamin D supplementation and sun safety."
    }
})

country_adaptations.update({
    "United States": {
        "Adaptation Mechanisms": "Diverse range of skin pigmentation due to mixed ancestry and varied UV exposure by region.",
        "Historical Context": "Lighter skin tones are more common in northern regions, while darker tones are prevalent in the south.",
        "Modern Challenges": "Vitamin D deficiency is common in northern areas, especially during winter.",
        "Exceptions": "Skin cancer risks are higher in fair-skinned populations, especially in areas with high UV exposure.",
        "Impact of Lifestyle": "Widespread use of sunscreen and vitamin D supplements, with public health campaigns promoting sun protection."
    },
    "Canada": {
        "Adaptation Mechanisms": "Lower melanin levels in indigenous and European-descended populations to aid vitamin D synthesis in low UV environments.",
        "Historical Context": "Lighter skin tones evolved in response to low UV exposure and long winters.",
        "Modern Challenges": "Vitamin D deficiency is common due to low natural sunlight exposure in winter.",
        "Exceptions": "Immigrant populations with darker skin may require additional vitamin D supplementation.",
        "Impact of Lifestyle": "Vitamin D supplements and fortified foods are widely available and recommended."
    },
    "Mexico": {
        "Adaptation Mechanisms": "Moderate to darker pigmentation levels across the country, adapted to varied UV exposure.",
        "Historical Context": "Indigenous populations developed darker skin suited for high UV in southern regions.",
        "Modern Challenges": "Urban lifestyles reduce natural UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Fair-skinned populations of European descent face higher UV sensitivity.",
        "Impact of Lifestyle": "Increased public awareness of sun protection and vitamin D supplementation."
    },
    "Brazil": {
        "Adaptation Mechanisms": "Diverse skin pigmentation across the country due to varied ancestry and UV exposure.",
        "Historical Context": "Darker skin tones in indigenous populations adapted to high UV exposure, especially in the Amazon.",
        "Modern Challenges": "Urban migration reduces natural sunlight exposure, resulting in vitamin D deficiency risks.",
        "Exceptions": "Fair-skinned populations are at higher risk of UV damage, especially in southern Brazil.",
        "Impact of Lifestyle": "Public campaigns promote sun protection and vitamin D awareness, particularly in high UV areas."
    },
    "Argentina": {
        "Adaptation Mechanisms": "Varied pigmentation, with darker tones in the north and lighter in the south.",
        "Historical Context": "Adapted to UV levels from tropical regions in the north to temperate regions in the south.",
        "Modern Challenges": "Urban lifestyles contribute to vitamin D deficiency, especially in winter.",
        "Exceptions": "European-descendant populations with fair skin are more susceptible to UV damage.",
        "Impact of Lifestyle": "Public health efforts focus on sun safety and vitamin D supplementation."
    },
    "Chile": {
        "Adaptation Mechanisms": "Varied pigmentation due to high altitudes in the Andes and lower UV levels in the south.",
        "Historical Context": "Indigenous Andean populations adapted to high UV at altitude with darker skin.",
        "Modern Challenges": "Urbanization leads to vitamin D deficiency due to reduced natural sunlight exposure.",
        "Exceptions": "Coastal populations receive less UV than high-altitude Andean regions.",
        "Impact of Lifestyle": "Public health efforts promote awareness of vitamin D supplementation and sun protection."
    },
    "Peru": {
        "Adaptation Mechanisms": "Higher melanin levels in Andean populations to cope with high UV at altitude.",
        "Historical Context": "Darker skin evolved to protect against intense UV exposure in the Andes.",
        "Modern Challenges": "Vitamin D deficiency is a growing issue in urban and coastal populations.",
        "Exceptions": "High-altitude Andean regions experience much higher UV exposure than coastal areas.",
        "Impact of Lifestyle": "Public health campaigns focus on vitamin D awareness and sun safety, especially in urban areas."
    },
    "Colombia": {
        "Adaptation Mechanisms": "Diverse skin pigmentation adapted to tropical and high-altitude UV exposure.",
        "Historical Context": "Populations in tropical lowlands and high-altitude Andes evolved varied skin tones.",
        "Modern Challenges": "Vitamin D deficiency is a concern in urban populations with limited sunlight.",
        "Exceptions": "High-altitude Andean populations face greater UV exposure than those in lower regions.",
        "Impact of Lifestyle": "Increased awareness of vitamin D supplementation and sunscreen use, particularly in urban areas."
    },
    "Venezuela": {
        "Adaptation Mechanisms": "Higher melanin levels in lowland regions to cope with intense tropical UV.",
        "Historical Context": "Dark pigmentation in indigenous populations developed as protection against equatorial sun.",
        "Modern Challenges": "Urbanization reduces natural UV exposure, impacting vitamin D levels.",
        "Exceptions": "Coastal and high-altitude populations experience different levels of UV exposure.",
        "Impact of Lifestyle": "Public health campaigns focus on sun protection and vitamin D awareness."
    },
    "Ecuador": {
        "Adaptation Mechanisms": "Higher melanin levels in lowland and coastal populations for UV protection.",
        "Historical Context": "Adapted to high UV levels in tropical and equatorial regions.",
        "Modern Challenges": "Urban lifestyles reduce sunlight exposure, contributing to vitamin D deficiency.",
        "Exceptions": "High-altitude Andean populations face even higher UV exposure than lowland regions.",
        "Impact of Lifestyle": "Increasing public health focus on sun safety and vitamin D supplementation in urban areas."
    },
    "Bolivia": {
        "Adaptation Mechanisms": "Darker skin tones in Andean regions adapted to intense UV at high altitude.",
        "Historical Context": "Populations developed darker pigmentation for UV protection in the Andes.",
        "Modern Challenges": "Vitamin D deficiency in urban populations due to indoor lifestyles.",
        "Exceptions": "Lowland populations experience less intense UV exposure than high-altitude areas.",
        "Impact of Lifestyle": "Public health initiatives on vitamin D and sunscreen usage are increasing."
    },
    "Paraguay": {
        "Adaptation Mechanisms": "Moderate to dark pigmentation adapted to subtropical and tropical UV exposure.",
        "Historical Context": "Indigenous populations developed pigmentation suitable for high UV exposure.",
        "Modern Challenges": "Vitamin D deficiency is growing in urban areas with reduced sunlight.",
        "Exceptions": "Lighter-skinned populations in urban centers face higher UV sensitivity.",
        "Impact of Lifestyle": "Increased awareness of sun protection and vitamin D, especially in urban regions."
    },
    "Uruguay": {
        "Adaptation Mechanisms": "Moderate skin pigmentation adapted to temperate climate with seasonal UV changes.",
        "Historical Context": "Adapted to UV exposure along coastal and temperate regions.",
        "Modern Challenges": "Urban lifestyles and indoor work contribute to vitamin D deficiency.",
        "Exceptions": "European-descendant populations may face higher risks of UV damage.",
        "Impact of Lifestyle": "Public health initiatives promote sunscreen and vitamin D supplementation."
    },
    "Costa Rica": {
        "Adaptation Mechanisms": "Higher melanin levels suited for tropical UV exposure.",
        "Historical Context": "Dark pigmentation evolved in indigenous populations as a natural defense against UV.",
        "Modern Challenges": "Urbanization has led to decreased natural sunlight exposure, impacting vitamin D levels.",
        "Exceptions": "People with albinism face significant UV-related health risks.",
        "Impact of Lifestyle": "Public health awareness on vitamin D and sunscreen is increasing, particularly in urban areas."
    },
    "Panama": {
        "Adaptation Mechanisms": "Higher melanin levels provide protection from intense equatorial sun.",
        "Historical Context": "Populations developed dark skin as a natural defense against tropical UV radiation.",
        "Modern Challenges": "Urban migration leads to vitamin D deficiency due to reduced outdoor UV exposure.",
        "Exceptions": "Coastal populations continue to have high sun exposure compared to urban areas.",
        "Impact of Lifestyle": "Public health campaigns emphasize balanced sun exposure and vitamin D awareness."
    },
    "Guatemala": {
        "Adaptation Mechanisms": "Higher melanin levels provide UV protection in tropical environments.",
        "Historical Context": "Dark skin pigmentation evolved as a natural defense against intense sunlight.",
        "Modern Challenges": "Vitamin D deficiency is increasing in urban populations due to reduced UV exposure.",
        "Exceptions": "Rural populations maintain higher levels of outdoor UV exposure.",
        "Impact of Lifestyle": "Growing awareness of vitamin D and sun safety, especially in cities."
    },
    "Honduras": {
        "Adaptation Mechanisms": "Higher melanin levels provide protection against tropical UV.",
        "Historical Context": "Adapted to high humidity and intense UV along coastal areas.",
        "Modern Challenges": "Vitamin D deficiency is common in urban areas with reduced sunlight exposure.",
        "Exceptions": "Rural and coastal populations receive more natural sunlight than urban areas.",
        "Impact of Lifestyle": "Public health campaigns focus on vitamin D and sun safety in urban areas."
    },
    "El Salvador": {
        "Adaptation Mechanisms": "Higher melanin levels adapted to high UV exposure in tropical regions.",
        "Historical Context": "Populations developed darker skin as a defense against intense sunlight.",
        "Modern Challenges": "Urbanization and indoor work contribute to vitamin D deficiency.",
        "Exceptions": "Rural populations still receive significant natural sunlight.",
        "Impact of Lifestyle": "Vitamin D awareness is growing, with public health focus on balanced sun exposure."
    },
    "Nicaragua": {
        "Adaptation Mechanisms": "Moderate to dark pigmentation adapted to tropical UV levels.",
        "Historical Context": "Dark skin pigmentation evolved to protect against strong UV in tropical regions.",
        "Modern Challenges": "Urban lifestyles reduce natural sunlight exposure, impacting vitamin D levels.",
        "Exceptions": "Rural populations are more exposed to natural sunlight.",
        "Impact of Lifestyle": "Public health initiatives focus on vitamin D and sun safety in urban centers."
    },
    "Cuba": {
        "Adaptation Mechanisms": "Higher melanin levels adapted to tropical climate with intense sunlight.",
        "Historical Context": "Dark skin pigmentation in indigenous populations developed to protect against high UV levels.",
        "Modern Challenges": "Vitamin D deficiency is growing in urban areas due to reduced sunlight.",
        "Exceptions": "Coastal populations receive higher natural UV exposure.",
        "Impact of Lifestyle": "Increased awareness of sunscreen use and vitamin D supplementation."
    },
    "Jamaica": {
        "Adaptation Mechanisms": "High melanin levels in indigenous populations provide protection against tropical UV.",
        "Historical Context": "Dark pigmentation adapted to consistent UV radiation in equatorial climate.",
        "Modern Challenges": "Urban migration reduces natural sunlight exposure, impacting vitamin D.",
        "Exceptions": "People with albinism face significant UV-related health risks.",
        "Impact of Lifestyle": "Public awareness of sun safety and vitamin D is increasing, especially in urban areas."
    },
    "Haiti": {
        "Adaptation Mechanisms": "Higher melanin levels provide protection against intense tropical sun exposure.",
        "Historical Context": "Dark skin pigmentation evolved as a natural defense against UV radiation.",
        "Modern Challenges": "Urban lifestyles with limited outdoor exposure increase vitamin D deficiency risks.",
        "Exceptions": "Rural populations receive more natural UV exposure than urban areas.",
        "Impact of Lifestyle": "Increased focus on vitamin D and sunscreen use in urban settings."
    },
    "Dominican Republic": {
        "Adaptation Mechanisms": "Higher melanin levels for protection against high tropical UV.",
        "Historical Context": "Dark pigmentation evolved in populations living in equatorial regions with high UV exposure.",
        "Modern Challenges": "Urbanization reduces natural UV exposure, leading to potential vitamin D deficiency.",
        "Exceptions": "Rural populations experience greater natural sunlight exposure.",
        "Impact of Lifestyle": "Growing awareness of vitamin D and sun safety, especially in cities."
    }
})

country_adaptations.update({
    "China": {
        "Adaptation Mechanisms": "Varied melanin levels; northern populations have lighter skin, southern populations darker.",
        "Historical Context": "Adaptations to a diverse range of climates, from tropical south to temperate north.",
        "Modern Challenges": "Urban lifestyles and air pollution limit natural UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Rural populations retain more traditional sun exposure habits, reducing vitamin D deficiency risks.",
        "Impact of Lifestyle": "Increased vitamin D supplementation and fortified foods in urban areas."
    },
    "India": {
        "Adaptation Mechanisms": "Diverse pigmentation; darker skin in southern regions adapted to intense UV radiation.",
        "Historical Context": "Southern populations developed darker pigmentation to cope with high UV exposure.",
        "Modern Challenges": "Vitamin D deficiency is common due to urban migration and indoor lifestyles.",
        "Exceptions": "Lighter skin tones are found in northern areas, where UV exposure is lower.",
        "Impact of Lifestyle": "Public health initiatives promote vitamin D awareness and sun safety in urban areas."
    },
    "Japan": {
        "Adaptation Mechanisms": "Moderate melanin levels suited to seasonal UV levels in temperate climates.",
        "Historical Context": "Adaptations to moderate UV exposure, with lighter skin tones in the north and darker in the south.",
        "Modern Challenges": "Urban lifestyles contribute to vitamin D deficiency, especially in winter.",
        "Exceptions": "Higher skin cancer rates among fair-skinned individuals.",
        "Impact of Lifestyle": "Public health campaigns focus on vitamin D and sun protection awareness."
    },
    "South Korea": {
        "Adaptation Mechanisms": "Moderate pigmentation adapted to seasonal changes in UV exposure.",
        "Historical Context": "Adaptations to temperate climates with varied UV exposure by season.",
        "Modern Challenges": "Urbanization and pollution reduce natural UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Higher skin cancer rates among fair-skinned individuals.",
        "Impact of Lifestyle": "Vitamin D supplements and public health campaigns on sun protection."
    },
    "Vietnam": {
        "Adaptation Mechanisms": "Higher melanin levels provide protection against intense tropical UV.",
        "Historical Context": "Dark skin pigmentation evolved to cope with high UV levels near the equator.",
        "Modern Challenges": "Urbanization reduces natural sunlight exposure, contributing to vitamin D deficiency.",
        "Exceptions": "Rural populations are exposed to more natural sunlight than urban areas.",
        "Impact of Lifestyle": "Increased awareness of vitamin D and sun protection in urban centers."
    },
    "Indonesia": {
        "Adaptation Mechanisms": "Higher melanin levels adapted to tropical climates with consistent UV exposure.",
        "Historical Context": "Dark pigmentation evolved as natural protection against intense sun exposure.",
        "Modern Challenges": "Urban lifestyles lead to reduced outdoor UV exposure, increasing vitamin D deficiency risks.",
        "Exceptions": "Populations at higher altitudes may experience lower UV exposure.",
        "Impact of Lifestyle": "Public awareness of sun safety and vitamin D is on the rise."
    },
    "Thailand": {
        "Adaptation Mechanisms": "Higher melanin levels provide protection from intense UV radiation in tropical regions.",
        "Historical Context": "Populations evolved darker pigmentation suited for high UV exposure.",
        "Modern Challenges": "Urbanization leads to vitamin D deficiency due to limited natural UV exposure.",
        "Exceptions": "Populations in rural areas are less likely to experience vitamin D deficiency.",
        "Impact of Lifestyle": "Increased public health campaigns on sun protection and vitamin D awareness."
    },
    "Malaysia": {
        "Adaptation Mechanisms": "High melanin levels adapted to intense tropical UV exposure.",
        "Historical Context": "Dark skin pigmentation evolved to protect against equatorial sun.",
        "Modern Challenges": "Urban migration reduces natural UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Rural populations continue to receive high natural sunlight exposure.",
        "Impact of Lifestyle": "Increased awareness of vitamin D and sunscreen usage in urban centers."
    },
    "Pakistan": {
        "Adaptation Mechanisms": "Varied pigmentation, with darker skin in southern regions and lighter in mountainous northern areas.",
        "Historical Context": "Adapted to diverse UV levels across tropical lowlands and cooler mountainous areas.",
        "Modern Challenges": "Urban lifestyles contribute to vitamin D deficiency.",
        "Exceptions": "Northern populations have lighter pigmentation and lower natural UV exposure.",
        "Impact of Lifestyle": "Increased use of vitamin D supplements and sun exposure awareness."
    },
    "Bangladesh": {
        "Adaptation Mechanisms": "Higher melanin levels provide protection against intense tropical UV exposure.",
        "Historical Context": "Adapted to high humidity and strong UV exposure, especially in coastal areas.",
        "Modern Challenges": "Urban migration reduces natural sunlight exposure, leading to vitamin D deficiency.",
        "Exceptions": "Rural populations experience more natural sunlight exposure.",
        "Impact of Lifestyle": "Growing awareness of vitamin D and sunscreen use, especially in cities."
    },
    "Philippines": {
        "Adaptation Mechanisms": "Higher melanin levels in native populations to cope with tropical UV exposure.",
        "Historical Context": "Dark pigmentation evolved as a natural defense against UV radiation in tropical climates.",
        "Modern Challenges": "Urbanization limits outdoor UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Coastal populations receive more natural sunlight than urban populations.",
        "Impact of Lifestyle": "Public health campaigns focus on sun protection and vitamin D awareness."
    },
    "Nepal": {
        "Adaptation Mechanisms": "High melanin levels among high-altitude populations adapted to strong UV at high altitudes.",
        "Historical Context": "Darker pigmentation in Himalayan regions evolved to cope with intense sunlight at altitude.",
        "Modern Challenges": "Vitamin D deficiency is common in urban and lower-altitude populations.",
        "Exceptions": "Lowland populations have lighter pigmentation and lower UV exposure.",
        "Impact of Lifestyle": "Increased focus on vitamin D supplementation and sun safety."
    },
    "Saudi Arabia": {
        "Adaptation Mechanisms": "Darker skin tones among indigenous populations to protect against intense desert UV.",
        "Historical Context": "Dark pigmentation evolved as a defense against the harsh desert sun.",
        "Modern Challenges": "Vitamin D deficiency is common due to limited sunlight exposure and cultural clothing practices.",
        "Exceptions": "Light-skinned populations are more susceptible to UV-related health risks.",
        "Impact of Lifestyle": "Growing use of vitamin D supplements and fortified foods."
    },
    "Iran": {
        "Adaptation Mechanisms": "Moderate pigmentation in desert and mountainous regions to protect from intense UV.",
        "Historical Context": "Adapted to high UV exposure in desert climates with darker skin tones.",
        "Modern Challenges": "Urbanization and cultural practices reduce natural UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Mountainous populations have slightly lighter skin tones.",
        "Impact of Lifestyle": "Increased vitamin D supplementation and sun safety awareness."
    },
    "Iraq": {
        "Adaptation Mechanisms": "Moderate to dark pigmentation adapted to desert UV exposure.",
        "Historical Context": "Darker skin tones evolved to cope with the intense UV in arid regions.",
        "Modern Challenges": "Vitamin D deficiency is prevalent due to limited outdoor exposure and cultural clothing.",
        "Exceptions": "Urbanized populations are at greater risk for vitamin D deficiency.",
        "Impact of Lifestyle": "Public health campaigns focus on vitamin D supplements and sun exposure."
    },
    "Turkey": {
        "Adaptation Mechanisms": "Moderate melanin levels suited to Mediterranean and varied UV exposure across regions.",
        "Historical Context": "Skin tones vary from lighter in the north to darker in the south.",
        "Modern Challenges": "Vitamin D deficiency in urbanized areas due to lower outdoor activity.",
        "Exceptions": "Fair-skinned individuals in the north face higher UV risks in southern regions.",
        "Impact of Lifestyle": "Public health initiatives focus on vitamin D awareness and sun safety."
    },
    "Afghanistan": {
        "Adaptation Mechanisms": "Darker skin tones in southern regions, lighter tones in mountainous areas.",
        "Historical Context": "Adaptations to UV levels in diverse environments, including deserts and highlands.",
        "Modern Challenges": "Urban migration reduces UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Highland populations experience different UV exposure than lowland regions.",
        "Impact of Lifestyle": "Public health efforts promote balanced sun exposure and vitamin D supplements."
    },
    "Israel": {
        "Adaptation Mechanisms": "Moderate pigmentation levels suited to Mediterranean and desert climates.",
        "Historical Context": "Adapted to moderate UV exposure, with lighter skin tones in some northern areas.",
        "Modern Challenges": "Urbanization reduces natural UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Northern populations with lighter skin tones face increased UV risks.",
        "Impact of Lifestyle": "Widespread sunscreen use and public health campaigns on vitamin D awareness."
    },
    "Jordan": {
        "Adaptation Mechanisms": "Moderate to darker pigmentation adapted to desert UV exposure.",
        "Historical Context": "Dark skin tones developed as a natural defense against desert sun.",
        "Modern Challenges": "Urbanization limits outdoor UV exposure, contributing to vitamin D deficiency.",
        "Exceptions": "Urban populations are at higher risk for vitamin D deficiency.",
        "Impact of Lifestyle": "Increased public health focus on vitamin D and sun safety."
    },
    "Lebanon": {
        "Adaptation Mechanisms": "Moderate melanin levels suited to Mediterranean climate and UV exposure.",
        "Historical Context": "Adapted to moderate UV, with lighter skin tones in the mountainous north.",
        "Modern Challenges": "Vitamin D deficiency is rising, especially in urban settings.",
        "Exceptions": "Southern populations have slightly darker skin tones due to higher UV exposure.",
        "Impact of Lifestyle": "Increased awareness of sun protection and vitamin D supplementation."
    },
    "Sri Lanka": {
        "Adaptation Mechanisms": "Higher melanin levels in native populations adapted to high UV tropical environment.",
        "Historical Context": "Dark pigmentation evolved as a defense against intense sunlight.",
        "Modern Challenges": "Urban migration leads to vitamin D deficiency due to reduced natural sunlight.",
        "Exceptions": "Coastal populations experience greater natural sunlight exposure than urban areas.",
        "Impact of Lifestyle": "Public health efforts focus on vitamin D awareness and sun protection."
    }
})

country_adaptations.update({
    "Australia": {
        "Adaptation Mechanisms": "Indigenous populations have high melanin levels adapted to intense UV radiation.",
        "Historical Context": "Aboriginal Australians evolved darker skin as a natural defense against high UV exposure.",
        "Modern Challenges": "Vitamin D deficiency is prevalent in urban areas due to indoor lifestyles.",
        "Exceptions": "Non-indigenous Australians with lighter skin face higher UV-related health risks.",
        "Impact of Lifestyle": "Strong public health campaigns emphasize sun protection, especially with high skin cancer rates."
    },
    "New Zealand": {
        "Adaptation Mechanisms": "Lighter skin tones among European-descended populations; indigenous Maori have darker skin.",
        "Historical Context": "Indigenous Maori populations evolved darker pigmentation for UV protection.",
        "Modern Challenges": "High skin cancer rates among fair-skinned populations due to high UV levels.",
        "Exceptions": "Maori populations have natural UV protection, reducing skin cancer risks.",
        "Impact of Lifestyle": "Public health campaigns on sun safety are highly prevalent, with emphasis on sunscreen use."
    },
    "Fiji": {
        "Adaptation Mechanisms": "Higher melanin levels in indigenous populations provide natural protection against high UV levels.",
        "Historical Context": "Adapted to high UV exposure in tropical environments.",
        "Modern Challenges": "Urban migration reduces natural sunlight exposure, contributing to vitamin D deficiency.",
        "Exceptions": "Rural populations continue to receive high UV exposure.",
        "Impact of Lifestyle": "Increasing awareness of vitamin D and sun safety, especially in urban centers."
    },
    "Papua New Guinea": {
        "Adaptation Mechanisms": "High melanin levels protect against intense tropical UV radiation.",
        "Historical Context": "Darker pigmentation evolved as a natural defense against high UV levels in equatorial regions.",
        "Modern Challenges": "Vitamin D deficiency is less common due to outdoor lifestyles in rural areas.",
        "Exceptions": "People with albinism face significant UV-related health risks.",
        "Impact of Lifestyle": "Increased public health focus on vitamin D supplementation in urbanized areas."
    },
    "Samoa": {
        "Adaptation Mechanisms": "Higher melanin levels protect indigenous populations from tropical UV exposure.",
        "Historical Context": "Dark skin pigmentation evolved to provide natural UV protection.",
        "Modern Challenges": "Vitamin D deficiency is becoming more common with urbanization and reduced sun exposure.",
        "Exceptions": "Rural areas experience higher natural sunlight exposure than urban areas.",
        "Impact of Lifestyle": "Public health campaigns on vitamin D and sun safety are increasing, especially in cities."
    },
    "Tonga": {
        "Adaptation Mechanisms": "High melanin levels in native populations provide UV protection in tropical climates.",
        "Historical Context": "Adapted to high UV exposure in a tropical environment.",
        "Modern Challenges": "Urban migration and reduced outdoor activity contribute to vitamin D deficiency.",
        "Exceptions": "Rural populations receive higher levels of natural sunlight exposure.",
        "Impact of Lifestyle": "Growing awareness of sun protection and vitamin D supplementation in urban areas."
    },
    "Vanuatu": {
        "Adaptation Mechanisms": "High melanin levels in native populations provide natural UV protection in tropical regions.",
        "Historical Context": "Darker pigmentation evolved to shield against consistent, intense sunlight.",
        "Modern Challenges": "Vitamin D deficiency is growing in urban areas with limited sun exposure.",
        "Exceptions": "Rural populations are exposed to more natural UV, reducing deficiency risks.",
        "Impact of Lifestyle": "Public health focus on vitamin D and sun protection is increasing, especially in urban centers."
    },
    "Solomon Islands": {
        "Adaptation Mechanisms": "High melanin levels adapted to high tropical UV exposure.",
        "Historical Context": "Dark pigmentation in indigenous populations developed to cope with intense sun.",
        "Modern Challenges": "Urban migration and reduced sun exposure increase risks of vitamin D deficiency.",
        "Exceptions": "Coastal populations experience high levels of natural UV exposure.",
        "Impact of Lifestyle": "Increased focus on vitamin D supplementation and sun safety, especially in urban areas."
    },
    "Micronesia": {
        "Adaptation Mechanisms": "Higher melanin levels in native populations provide UV protection in equatorial climate.",
        "Historical Context": "Darker skin pigmentation evolved to protect against tropical UV exposure.",
        "Modern Challenges": "Vitamin D deficiency is more common in urbanized areas with reduced sunlight exposure.",
        "Exceptions": "Rural populations retain higher natural sun exposure.",
        "Impact of Lifestyle": "Increasing public health campaigns on vitamin D awareness and sun safety in cities."
    },
    "Palau": {
        "Adaptation Mechanisms": "Higher melanin levels provide natural protection against UV radiation in tropical climates.",
        "Historical Context": "Dark pigmentation developed as a natural defense against UV exposure.",
        "Modern Challenges": "Urban migration and reduced outdoor activity increase risks of vitamin D deficiency.",
        "Exceptions": "Rural populations maintain higher sun exposure levels.",
        "Impact of Lifestyle": "Vitamin D awareness and sunscreen use are emphasized in public health initiatives."
    },
    "Marshall Islands": {
        "Adaptation Mechanisms": "Higher melanin levels help protect native populations against intense tropical UV.",
        "Historical Context": "Dark skin pigmentation evolved as a natural shield against UV radiation.",
        "Modern Challenges": "Vitamin D deficiency risks are growing with urbanization and reduced outdoor activity.",
        "Exceptions": "Coastal and rural populations experience greater natural UV exposure.",
        "Impact of Lifestyle": "Public health efforts focus on vitamin D and sunscreen use, especially in urban areas."
    },
    "Kiribati": {
        "Adaptation Mechanisms": "High melanin levels in indigenous populations adapted to intense tropical UV radiation.",
        "Historical Context": "Dark pigmentation developed as a natural protection against UV radiation near the equator.",
        "Modern Challenges": "Urban lifestyles lead to vitamin D deficiency due to limited sun exposure.",
        "Exceptions": "Rural populations are exposed to higher levels of natural UV.",
        "Impact of Lifestyle": "Growing public awareness on vitamin D and sun safety, especially in urban settings."
    },
    "Tuvalu": {
        "Adaptation Mechanisms": "Higher melanin levels protect against UV radiation in a tropical environment.",
        "Historical Context": "Dark pigmentation evolved as a natural shield against intense sunlight near the equator.",
        "Modern Challenges": "Urbanization leads to vitamin D deficiency risks due to reduced sun exposure.",
        "Exceptions": "Rural populations maintain higher sun exposure and are less prone to deficiency.",
        "Impact of Lifestyle": "Public health campaigns on vitamin D and sun protection are growing in urban areas."
    },
    "Nauru": {
        "Adaptation Mechanisms": "High melanin levels adapted to intense tropical UV exposure.",
        "Historical Context": "Dark skin pigmentation developed to cope with high UV levels in a tropical climate.",
        "Modern Challenges": "Vitamin D deficiency is increasing with urbanization and indoor work.",
        "Exceptions": "Rural and coastal populations experience higher natural UV exposure.",
        "Impact of Lifestyle": "Increasing emphasis on sun safety and vitamin D awareness, especially in cities."
    },
    "French Polynesia": {
        "Adaptation Mechanisms": "High melanin levels provide natural UV protection in tropical environments.",
        "Historical Context": "Darker skin pigmentation evolved to protect against intense sunlight.",
        "Modern Challenges": "Urban migration reduces natural UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Rural populations receive more natural UV exposure than urban populations.",
        "Impact of Lifestyle": "Public health efforts focus on vitamin D and sun protection awareness."
    },
    "New Caledonia": {
        "Adaptation Mechanisms": "Higher melanin levels provide protection from tropical UV radiation.",
        "Historical Context": "Dark pigmentation evolved as a natural adaptation to high UV exposure.",
        "Modern Challenges": "Vitamin D deficiency is becoming more common with urbanization.",
        "Exceptions": "Rural and coastal populations have higher sun exposure than urban areas.",
        "Impact of Lifestyle": "Increased focus on vitamin D supplementation and sun safety in public health initiatives."
    }
})

country_adaptations.update({
    "Nigeria": {
        "Adaptation Mechanisms": "High melanin levels provide natural protection against intense UV in tropical climates.",
        "Historical Context": "Dark pigmentation evolved to protect against equatorial sun exposure.",
        "Modern Challenges": "Urban migration leads to vitamin D deficiency due to reduced outdoor activity.",
        "Exceptions": "People with albinism face significant UV-related health risks.",
        "Impact of Lifestyle": "Increasing awareness of sunscreen and vitamin D supplementation in urban areas."
    },
    "South Africa": {
        "Adaptation Mechanisms": "Varied skin tones, with higher melanin levels in native populations for UV protection.",
        "Historical Context": "Dark pigmentation developed as a defense against high UV in some regions.",
        "Modern Challenges": "Urban lifestyles contribute to vitamin D deficiency due to reduced sunlight exposure.",
        "Exceptions": "Lighter-skinned individuals are more susceptible to UV damage in high-sun regions.",
        "Impact of Lifestyle": "Public health campaigns promote sun safety and vitamin D awareness."
    },
    "Kenya": {
        "Adaptation Mechanisms": "Higher melanin levels among indigenous populations adapted to intense equatorial sun.",
        "Historical Context": "Dark skin evolved to protect against high UV near the equator.",
        "Modern Challenges": "Vitamin D deficiency is becoming more common with urban migration.",
        "Exceptions": "People with albinism face significant UV-related health challenges.",
        "Impact of Lifestyle": "Public health efforts focus on sun protection and vitamin D awareness in urban areas."
    },
    "Egypt": {
        "Adaptation Mechanisms": "Darker skin tones evolved in indigenous populations for protection against desert UV levels.",
        "Historical Context": "Dark pigmentation adapted to intense sunlight, especially in desert areas.",
        "Modern Challenges": "Urbanization reduces outdoor UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "Fair-skinned individuals face higher risks of UV damage.",
        "Impact of Lifestyle": "Sunscreen and vitamin D supplementation awareness is growing in urban areas."
    },
    "Ethiopia": {
        "Adaptation Mechanisms": "Higher melanin levels provide protection against high UV exposure, especially in lowland areas.",
        "Historical Context": "Adapted to intense sun exposure near the equator with darker pigmentation.",
        "Modern Challenges": "Vitamin D deficiency is less common in rural areas but is growing in urban areas.",
        "Exceptions": "People with albinism face increased UV risks.",
        "Impact of Lifestyle": "Public health initiatives emphasize sun safety and vitamin D in urban settings."
    },
    "Sudan": {
        "Adaptation Mechanisms": "Dark skin tones evolved to provide natural UV protection in desert and equatorial climates.",
        "Historical Context": "Adaptations to intense sun exposure in arid and tropical regions.",
        "Modern Challenges": "Urban migration reduces UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "People with albinism face significant health risks due to UV exposure.",
        "Impact of Lifestyle": "Public health campaigns promote sunscreen use and vitamin D awareness."
    },
    "Morocco": {
        "Adaptation Mechanisms": "Moderate to dark skin tones adapted to Mediterranean and desert UV levels.",
        "Historical Context": "Populations evolved darker skin tones in response to high sun exposure.",
        "Modern Challenges": "Vitamin D deficiency is common in urbanized populations with limited sunlight.",
        "Exceptions": "Lighter-skinned populations face higher UV sensitivity.",
        "Impact of Lifestyle": "Vitamin D supplementation and sun protection are emphasized in health campaigns."
    },
    "Ghana": {
        "Adaptation Mechanisms": "Higher melanin levels provide natural protection from intense equatorial sun exposure.",
        "Historical Context": "Dark skin pigmentation developed to cope with high UV exposure in tropical climates.",
        "Modern Challenges": "Vitamin D deficiency is increasing in urban areas with reduced sunlight.",
        "Exceptions": "People with albinism face significant health risks from UV exposure.",
        "Impact of Lifestyle": "Public health campaigns focus on sun safety and vitamin D supplementation in cities."
    },
    "Tanzania": {
        "Adaptation Mechanisms": "Higher melanin levels provide UV protection, especially in equatorial and highland regions.",
        "Historical Context": "Adapted to intense sunlight near the equator with darker skin pigmentation.",
        "Modern Challenges": "Vitamin D deficiency is growing in urban populations due to indoor lifestyles.",
        "Exceptions": "Albinism is prevalent, leading to increased UV-related health challenges.",
        "Impact of Lifestyle": "Public health initiatives focus on sun protection and vitamin D awareness."
    },
    "Uganda": {
        "Adaptation Mechanisms": "Higher melanin levels in indigenous populations provide protection from intense UV radiation.",
        "Historical Context": "Adapted to consistent, intense sun exposure near the equator.",
        "Modern Challenges": "Vitamin D deficiency is increasing with urban migration and indoor work.",
        "Exceptions": "Rural populations maintain higher sun exposure and lower deficiency risks.",
        "Impact of Lifestyle": "Public health campaigns emphasize sun protection and vitamin D supplementation in cities."
    },
    "Rwanda": {
        "Adaptation Mechanisms": "High melanin levels provide natural UV protection in tropical and equatorial climates.",
        "Historical Context": "Darker skin pigmentation evolved as a natural defense against UV radiation.",
        "Modern Challenges": "Urban migration and limited sunlight exposure contribute to vitamin D deficiency.",
        "Exceptions": "People with albinism are at high risk for UV-related health issues.",
        "Impact of Lifestyle": "Public health initiatives promote vitamin D awareness and sun safety."
    },
    "Algeria": {
        "Adaptation Mechanisms": "Moderate to darker pigmentation developed as a natural defense against high desert UV.",
        "Historical Context": "Adapted to intense sun exposure in arid and desert regions.",
        "Modern Challenges": "Vitamin D deficiency is common due to limited outdoor exposure in urban areas.",
        "Exceptions": "Fair-skinned populations are more susceptible to UV damage.",
        "Impact of Lifestyle": "Public health campaigns promote vitamin D supplementation and sun safety."
    },
    "Democratic Republic of the Congo": {
        "Adaptation Mechanisms": "High melanin levels provide protection from intense UV radiation in tropical climates.",
        "Historical Context": "Darker pigmentation evolved to cope with strong UV exposure near the equator.",
        "Modern Challenges": "Urban migration reduces natural UV exposure, leading to vitamin D deficiency.",
        "Exceptions": "People with albinism face significant UV-related health risks.",
        "Impact of Lifestyle": "Growing awareness of vitamin D and sun safety in urban centers."
    },
    "Angola": {
        "Adaptation Mechanisms": "Higher melanin levels provide protection against high UV levels in tropical climates.",
        "Historical Context": "Dark pigmentation evolved as a defense against intense sunlight.",
        "Modern Challenges": "Vitamin D deficiency is becoming more common in urban areas.",
        "Exceptions": "Rural populations are less affected due to consistent natural sun exposure.",
        "Impact of Lifestyle": "Increased public health focus on vitamin D supplementation and sun protection in cities."
    },
    "Zimbabwe": {
        "Adaptation Mechanisms": "Higher melanin levels provide protection against strong UV radiation in tropical and highland areas.",
        "Historical Context": "Adaptations to intense sunlight exposure, particularly in highland regions.",
        "Modern Challenges": "Vitamin D deficiency is growing in urbanized populations.",
        "Exceptions": "People with albinism face increased risks from UV exposure.",
        "Impact of Lifestyle": "Public health campaigns promote awareness of sun safety and vitamin D."
    },
    "Ivory Coast": {
        "Adaptation Mechanisms": "High melanin levels provide natural UV protection in tropical regions.",
        "Historical Context": "Dark skin pigmentation developed to cope with consistent high UV exposure.",
        "Modern Challenges": "Vitamin D deficiency is becoming more common due to urban migration.",
        "Exceptions": "Rural populations retain higher sun exposure and are less prone to deficiency.",
        "Impact of Lifestyle": "Public health efforts focus on vitamin D awareness and sun safety."
    },
    "Senegal": {
        "Adaptation Mechanisms": "High melanin levels provide UV protection in tropical and equatorial climates.",
        "Historical Context": "Dark pigmentation evolved to protect against intense UV radiation.",
        "Modern Challenges": "Vitamin D deficiency is common in urban areas due to reduced sunlight exposure.",
        "Exceptions": "Rural populations are more naturally exposed to UV.",
        "Impact of Lifestyle": "Increased public health campaigns on vitamin D supplementation and sun safety."
    },
    "Somalia": {
        "Adaptation Mechanisms": "Darker skin tones evolved to protect against high UV exposure in desert climates.",
        "Historical Context": "Adapted to intense sunlight exposure in arid and tropical areas.",
        "Modern Challenges": "Urban migration and limited outdoor UV exposure increase vitamin D deficiency.",
        "Exceptions": "People with albinism face significant health risks due to UV exposure.",
        "Impact of Lifestyle": "Public health campaigns emphasize vitamin D and sunscreen use."
    },
    "Zambia": {
        "Adaptation Mechanisms": "Higher melanin levels provide protection from intense sunlight in tropical climates.",
        "Historical Context": "Dark pigmentation evolved to protect against high UV radiation near the equator.",
        "Modern Challenges": "Vitamin D deficiency is rising in urban populations with reduced sunlight exposure.",
        "Exceptions": "Rural populations experience more natural sunlight exposure.",
        "Impact of Lifestyle": "Public health campaigns focus on sun safety and vitamin D awareness in cities."
    },
    "Botswana": {
        "Adaptation Mechanisms": "High melanin levels provide protection against UV in arid and high UV regions.",
        "Historical Context": "Adapted to intense sunlight exposure, particularly in desert areas.",
        "Modern Challenges": "Vitamin D deficiency is common in urban settings with limited UV exposure.",
        "Exceptions": "People with albinism are at higher risk for UV-related health issues.",
        "Impact of Lifestyle": "Public health campaigns promote vitamin D and sun safety awareness."
    }
})

country_adaptations.update({
    "Iceland": {
        "Adaptation Mechanisms": "Very light skin tones evolved to maximize vitamin D synthesis in low UV conditions.",
        "Historical Context": "Populations adapted to extremely low sunlight exposure, especially during long winters.",
        "Modern Challenges": "Vitamin D deficiency is prevalent, particularly during winter months with minimal daylight.",
        "Exceptions": "Immigrants from regions with higher UV exposure may have greater vitamin D deficiency risks due to lower natural synthesis in Iceland.",
        "Impact of Lifestyle": "Widespread use of vitamin D supplements, with public health campaigns encouraging fortified foods and sun exposure whenever possible."
    }
})


app.layout = html.Div([
    html.Div(style={'display': 'flex', 'width': '100%'}, children=[
        html.Div(
            dcc.Graph(id='world-map', figure=fig),
            style={'flex': '3', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'margin': '20px'}
        ),
        html.Div(id='info-box', style={
            'flex': '1', 
            'display': 'flex', 
            'justify-content': 'center', 
            'align-items': 'center', 
            'padding': '20px',
            'background-color': 'rgba(240, 240, 240, 0.9)',
            'border-radius': '8px'
        }, children=[
            html.Div(id='info-content', children=[
                html.H2(id='country-name', style={'text-align': 'center', 'font-size': '24px', 'margin-bottom': '10px'}),
                html.Div(id='country-info', style={
                    'text-align': 'center', 
                    'font-size': '18px', 
                    'padding': '10px'
                })  # Display country info as non-editable text
            ])
        ])
    ])
])

@app.callback(
    [Output('country-name', 'children'),
     Output('country-info', 'children')],
    Input('world-map', 'clickData')
)
def display_info(clickData):
    if clickData is None:
        return '', 'Click on a country to view adaptations.'
    else:
        country = clickData['points'][0]['hovertext']
        info_dict = country_adaptations.get(country, {
            "Adaptation Mechanisms": "No information available.",
            "Historical Context": "No information available.",
            "Modern Challenges": "No information available.",
            "Exceptions": "No information available.",
            "Impact of Lifestyle": "No information available."
        })

        # Convert the dictionary to a formatted string for display
        info_text = "\n\n".join([f"**{key}:** {value}" for key, value in info_dict.items()])

        return f"Adaptations in {country}", dcc.Markdown(info_text)


if __name__ == '__main__':
    app.run_server(debug=True)
