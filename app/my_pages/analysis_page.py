import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import pandas as pd
from utils.helpers import format_number, AIRBNB_COLORS

def show(logo_base64):
    if 'data_cleaned' not in st.session_state: 
        st.warning("Bitte lade zuerst eine CSV-Datei hoch und bereinige die Daten auf der Seite 'CSV-Datei hochladen'.") 
    else: 
        # Bereinigte Daten aus st.session_state laden 
        data = st.session_state['data_cleaned']
        # Stand des DataFrames aus der Spalte "last_review" anzeigen: ältester Wert
        if 'last_review' in data.columns:
            first_review_date = pd.to_datetime(data['last_review']).min()
            last_review_date = pd.to_datetime(data['last_review']).max()
            st.success(f"✅ Hinweis: Die Daten in diesem Dashboard decken den Zeitraum vom {first_review_date.strftime('%d.%m.%Y')} bis {last_review_date.strftime('%d.%m.%Y')} ab.")
        # Filter-Bereich in einem Expander 
        with st.expander("Filter", expanded=True): 
            col1, col2 = st.columns(2)
            with col1:
                neighbourhood_group = st.selectbox( 
                    "Wähle eine Nachbarschaftsgruppe:", 
                    options=["Alle"] + sorted(data['neighbourhood_group'].dropna().unique().tolist()) 
                ) 
                if 'neighbourhood' in data.columns:
                    if neighbourhood_group != "Alle":
                        neighbourhood_options = data[data['neighbourhood_group'] == neighbourhood_group]['neighbourhood'].unique() 
                    else:
                        neighbourhood_options = data['neighbourhood'].unique() 
                    neighbourhood = st.selectbox( 
                        "Wähle eine Nachbarschaft:", 
                        options=["Alle"] + sorted(neighbourhood_options) 
                    )
                else:
                    neighbourhood = "Alle"  
            with col2:
                room_type = st.selectbox( 
                    "Wähle einen Zimmer-Typ:", 
                    options=["Alle"] + sorted(data['room_type'].dropna().unique().tolist()) 
                ) 
                min_price = int(data['price'].min()) 
                max_price = int(data['price'].max()) 
                price_range = st.slider( 
                    "Wähle einen Preisbereich:", 
                    min_value=min_price, 
                    max_value=max_price, 
                    value=(min_price, max_price)  
                ) 
        # Filtern der Daten basierend auf der Auswahl 
        filtered_data = data 
        if neighbourhood_group != "Alle": 
            filtered_data = filtered_data[filtered_data['neighbourhood_group'] == neighbourhood_group] 
        if neighbourhood != "Alle" and 'neighbourhood' in data.columns: 
            filtered_data = filtered_data[filtered_data['neighbourhood'] == neighbourhood] 
        if room_type != "Alle": 
            filtered_data = filtered_data[filtered_data['room_type'] == room_type] 
        filtered_data = filtered_data[ 
            (filtered_data['price'] >= price_range[0]) & (filtered_data['price'] <= price_range[1]) 
        ] 
        # Farbe basierend auf dem Preis festlegen 
        max_price_filtered = filtered_data['price'].max() 
        min_price_filtered = filtered_data['price'].min() 
        # Normalisiere den Preis für die Farbgebung (0-255) 
        def normalize_price(price): 
            if max_price_filtered == min_price_filtered:  
                return 128  
            return int((price - min_price_filtered) / (max_price_filtered - min_price_filtered) * 255) 
        # Farbe basierend auf dem Preis (AirBnB-Farben)
        filtered_data['color'] = filtered_data['price'].apply(
            lambda x: [255, 90, 95, 200]  
        )
        # Radius basierend auf dem Preis (größere Punkte für teurere Zimmer) 
        filtered_data['radius'] = filtered_data['price'].apply( 
            lambda x: 50 if max_price_filtered == min_price_filtered else  
            (x - min_price_filtered) / (max_price_filtered - min_price_filtered) * 200 + 50 
        ) 

        # Tooltip-Inhalt vorbereiten mit formatiertem Preis
        filtered_data['formatted_price'] = filtered_data['price'].apply(lambda x: format_number(x, 2))
        filtered_data['tooltip'] = filtered_data.apply(
            lambda row: {
                'price': f"{row['formatted_price']} ¤",  # Verwendet den formatierten Preis
                'room_type': row['room_type'],
                'neighbourhood_group': row['neighbourhood_group']
            },
            axis=1
        ) 

        # Statistiken Container
        st.subheader("📋 Übersicht")

        # Funktion zur Anzeige von Metriken
        def display_metrics(metrics, column):
            with column:
                for metric in metrics:
                    st.markdown(f"""
                    <div class="metric-card">
                        <p class="metric-label">{metric['icon']} {metric['label']}</p>
                        <p class="metric-value">{metric['value']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        # Berechnung der Statistiken
        total_listings = len(filtered_data)
        avg_price = filtered_data['price'].mean()
        avg_availability_365 = filtered_data['availability_365'].mean()
        median_price = filtered_data['price'].median()
        min_price_value = filtered_data['price'].min()
        max_price_value = filtered_data['price'].max()
        avg_min_nights = filtered_data['minimum_nights'].mean()
        sum_of_reviews = filtered_data['number_of_reviews'].sum()
        avg_number_of_reviews = filtered_data['number_of_reviews'].mean()

        # Erstelle zwei Spalten
        col1, col2, col3 = st.columns(3)
        # Linke Spalte
        metrics_left = [
            {"label": "Anzahl der Einträge", "value": f"{format_number(total_listings, 0)}", "icon": "🏠"},
            {"label": "Durchschnittlicher Preis", "value": f"{format_number(avg_price)} ¤", "icon": "💰"},
            {"label": "Niedrigster Preis", "value": f"{format_number(min_price_value)} ¤", "icon": "⬇️"}
        ]
        display_metrics(metrics_left, col1)
        # Mitllere Spalte
        metrics_right = [
            {"label": "Durchschnittliche Verfügbarkeit im Jahr", "value": f"{format_number(avg_availability_365)}", "icon": "📆"},
            {"label": "Durchschnittliche min. Übernachtungen", "value": f"{format_number(avg_min_nights, 1)} Nächte", "icon": "🌙"},
            {"label": "Höchster Preis", "value": f"{format_number(max_price_value)} ¤", "icon": "⬆️"}
        ]
        display_metrics(metrics_right, col2)

        # Rechte Spalte
        metrics_right = [
            {"label": "Summe Reviews", "value": f"{format_number(sum_of_reviews, 0)}", "icon": "🎤"},
            {"label": "Reviews im Durchschnitt", "value": f"{format_number(avg_number_of_reviews, 2)}", "icon": "📢"},
            {"label": "Median Preis", "value": f"{format_number(median_price)} ¤", "icon": "📊"}
        ]
        display_metrics(metrics_right, col3)

        # Karte mit pydeck anzeigen 
        st.subheader("🗺️ Karte")
        map_layer = pdk.Deck( 
            initial_view_state=pdk.ViewState( 
                latitude=filtered_data['latitude'].mean(), 
                longitude=filtered_data['longitude'].mean(), 
                zoom=10, 
                pitch=50 
            ), 
        layers=[ 
            pdk.Layer( 
                'ScatterplotLayer', 
                data=filtered_data, 
                get_position='[longitude, latitude]', 
                get_color='color', 
                get_radius='radius', 
                pickable=True, 
                opacity=0.8, 
            ) 
        ], 
        tooltip={
            "html": "<b>Preis:</b> {price} ¤<br/>"
                "<b>Zimmer-Typ:</b> {room_type}<br/>"
                "<b>Nachbarschaftsgruppe:</b> {neighbourhood_group}",
        "style": {
            "backgroundColor": AIRBNB_COLORS['primary'],
            "color": "white"
        }
    }
)       

        # Füge zuerst den CSS-Style hinzu
        st.markdown("""
        <style>
        .dark-container {
            background-color: #1E1E1E;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }

        .metric-card {
            background-color: #2D2D2D;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            margin: 10px 0;
            height: 100%;
        }

        .metric-label {
            font-size: 14px;
            color: #B0B0B0;
            margin-bottom: 5px;
        }

        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #FFFFFF;
            margin: 0;
        }

        .column-container {
            display: flex;
            gap: 20px;
        }

        .column {
            flex: 1;
            padding: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

        # Hauptcode
        st.pydeck_chart(map_layer)

        # Aggregation der Daten pro Nachbarschaftsgruppe 
        aggregated_data = filtered_data.groupby('neighbourhood_group').agg({ 
            'price': 'mean', 
            'minimum_nights': 'mean' 
        }).reset_index() 
        # Zahlen auf 2 Kommastellen runden 
        aggregated_data['price'] = aggregated_data['price'].round(2) 
        aggregated_data['minimum_nights'] = aggregated_data['minimum_nights'].round(2) 
        # Umbenennen der Spalten für die Anzeige 
        aggregated_data = aggregated_data.rename(columns={ 
            'neighbourhood_group': 'Nachbarschaftsgruppe', 
            'price': 'Durchschnittlicher Preis', 
            'minimum_nights': 'Durchschnittliche minimale Übernachtungen' 
        }) 
        
        # Anzeige der aggregierten Daten in einer Tabelle 
        # st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("📅 Durchschnittlicher Preis und minimale Übernachtungen pro Nachbarschaftsgruppe") 
        # st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(aggregated_data, use_container_width=True) 
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        # Visualisierung der aggregierten Daten in einem Diagramm 
        # st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        # st.header("Visualisierung der aggregierten Daten") 
        # Balkendiagramm für den durchschnittlichen Preis 
        # st.subheader("Durchschnittlicher Preis pro Nachbarschaftsgruppe") 

        st.subheader("🔍 Diagramme")
        fig_hist = px.histogram(
            filtered_data, 
            x="price", 
            nbins=50,
            title="Verteilung der Preise",
            labels={"price": "Preis (¤)"},
            color_discrete_sequence=[AIRBNB_COLORS['primary']]
        )

        fig_hist.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font={'color': AIRBNB_COLORS['light']},
            title_font_color=AIRBNB_COLORS['tertiary'],
            title={
            'text': "Verteilung der Preise",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
            xaxis_title_font=dict(color=AIRBNB_COLORS['light']),
            yaxis_title_font=dict(color=AIRBNB_COLORS['light']),
            xaxis=dict(
            tickfont=dict(color=AIRBNB_COLORS['light']),
            tickformat=",.",
            separatethousands=True
            ),
            yaxis=dict(tickfont=dict(color=AIRBNB_COLORS['light']))
        )

        # Liniendiagramm für den durchschnittlichen Preis über die Zeit
        if 'last_review' in filtered_data.columns:
            filtered_data['last_review'] = pd.to_datetime(filtered_data['last_review'])
            time_series_data = filtered_data.groupby(filtered_data['last_review'].dt.to_period('M')).agg({'price': 'mean'}).reset_index()
            time_series_data['last_review'] = time_series_data['last_review'].dt.to_timestamp()

            fig_line = px.line(
            time_series_data,
            x='last_review',
            y='price',
            title='Durchschnittlicher Preis über die Zeit',
            labels={'last_review': 'Datum', 'price': 'Durchschnittlicher Preis (¤)'},
            color_discrete_sequence=[AIRBNB_COLORS['primary']]
            )
            fig_line.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font={'color': AIRBNB_COLORS['light']},
            title_font_color=AIRBNB_COLORS['tertiary'],
            title={
                'text': "Durchschnittlicher Preis über die Zeit",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title_font=dict(color=AIRBNB_COLORS['light']),
            yaxis_title_font=dict(color=AIRBNB_COLORS['light']),
            xaxis=dict(tickfont=dict(color=AIRBNB_COLORS['light'])),
            yaxis=dict(tickfont=dict(color=AIRBNB_COLORS['light']))
            )
            st.plotly_chart(fig_line, use_container_width=True)
        fig_hist.update_traces(marker=dict(line=dict(color=AIRBNB_COLORS['dark'], width=1)))
    
        st.plotly_chart(fig_hist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


        fig1 = px.bar(
            aggregated_data, 
            x='Nachbarschaftsgruppe', 
            y='Durchschnittlicher Preis',
            title='Durchschnittlicher Preis pro Nachbarschaftsgruppe',
            color_discrete_sequence=[AIRBNB_COLORS['primary']]
        )
        fig1.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font={'color': AIRBNB_COLORS['light']},
            title_font_color=AIRBNB_COLORS['tertiary'],
            title={
            'text': "Durchschnittlicher Preis pro Nachbarschaftsgruppe",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
            xaxis_title_font=dict(color=AIRBNB_COLORS['light']),
            yaxis_title_font=dict(color=AIRBNB_COLORS['light']),
            xaxis=dict(tickfont=dict(color=AIRBNB_COLORS['light'])),
            yaxis=dict(tickfont=dict(color=AIRBNB_COLORS['light']))
        )
        # Formatierung der y-Achsen-Beschriftungen
        fig1.update_traces(
            texttemplate='%{y:,.2f} ¤'.replace('.', ','),
            textposition='outside'
        )
        fig1.update_yaxes(tickprefix='¤')

        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.bar(
        aggregated_data, 
        x='Nachbarschaftsgruppe', 
        y='Durchschnittliche minimale Übernachtungen',
        title='Durchschnittliche minimale Übernachtungen pro Nachbarschaftsgruppe',
        color_discrete_sequence=[AIRBNB_COLORS['secondary']]
        )
        fig2.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font={'color': AIRBNB_COLORS['light']},
            title_font_color=AIRBNB_COLORS['tertiary'],
            title={
            'text': "Durchschnittliche minimale Übernachtungen pro Nachbarschaftsgruppe",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
            xaxis_title_font=dict(color=AIRBNB_COLORS['dark']),
            yaxis_title_font=dict(color=AIRBNB_COLORS['dark']),
            xaxis=dict(tickfont=dict(color=AIRBNB_COLORS['dark'])),
            yaxis=dict(tickfont=dict(color=AIRBNB_COLORS['dark']))
        )
        # Formatierung der y-Achsen-Beschriftungen
        fig2.update_traces(
            texttemplate='%{y:,.2f}',
            textposition='outside'
        )
        fig2.update_yaxes(tickprefix='')
        fig2.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font={'color': AIRBNB_COLORS['light']},
            title_font_color=AIRBNB_COLORS['tertiary'],
            xaxis_title_font=dict(color=AIRBNB_COLORS['dark']),
            yaxis_title_font=dict(color=AIRBNB_COLORS['dark']),
            xaxis=dict(tickfont=dict(color=AIRBNB_COLORS['dark'])),
            yaxis=dict(tickfont=dict(color=AIRBNB_COLORS['dark']))
        )
        # Formatierung der y-Achsen-Beschriftungen
        fig2.update_traces(
            texttemplate='%{y:,.2f}',
            textposition='outside'
        )
        fig2.update_yaxes(tickprefix='')

        st.plotly_chart(fig2, use_container_width=True) 
        # Kuchendiagramm für die Aufteilung der Immobilien nach Immobilienart 
        # st.subheader("Aufteilung der Immobilien nach Immobilienart") 
        room_type_counts = filtered_data['room_type'].value_counts() 
        fig3 = px.pie(
            room_type_counts, 
            values=room_type_counts.values, 
            names=room_type_counts.index,
            title='Aufteilung der Immobilien nach Immobilienart', 
            hole=0.3,
            color_discrete_sequence=[AIRBNB_COLORS['primary'], AIRBNB_COLORS['secondary'], AIRBNB_COLORS['tertiary']]
        )
        fig3.update_layout(
            title={
            'text': "Aufteilung der Immobilien nach Immobilienart",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'color': AIRBNB_COLORS['tertiary']}
            },
            plot_bgcolor='black',
            paper_bgcolor='black',
            font={'color': AIRBNB_COLORS['light']}
        )

        st.plotly_chart(fig3, use_container_width=True)
        # Heatmap der Preise nach Nachbarschaftsgruppe und Zimmertyp
        if len(filtered_data) > 0 and len(filtered_data['neighbourhood_group'].unique()) > 1:
            # st.subheader("Heatmap: Durchschnittlicher Preis nach Nachbarschaftsgruppe und Zimmertyp")
            heatmap_data = filtered_data.pivot_table(
                values='price',
                index='neighbourhood_group',
                columns='room_type',
                aggfunc='mean'
            ).round(2)
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale=[[0, AIRBNB_COLORS['secondary']], [1, AIRBNB_COLORS['primary']]],
                text=[[format_number(val) + "¤" for val in row] for row in heatmap_data.values],
                texttemplate="%{text}",
                textfont={"size": 12}
            ))

            fig_heatmap.update_layout(
                title={
                    'text': "Durchschnittlicher Preis nach Nachbarschaftsgruppe und Zimmertyp",
                    'y': 0.9,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'color': AIRBNB_COLORS['tertiary']}
                },
                plot_bgcolor='black',
                paper_bgcolor='black',
                font={'color': AIRBNB_COLORS['light']},
                title_font_color=AIRBNB_COLORS['tertiary'],
                xaxis_title_font=dict(color=AIRBNB_COLORS['dark']),
                yaxis_title_font=dict(color=AIRBNB_COLORS['dark']),
                xaxis=dict(tickfont=dict(color=AIRBNB_COLORS['dark'])),
                yaxis=dict(tickfont=dict(color=AIRBNB_COLORS['dark']))
            )

            # Balkendiagramm für Anzahl der Reviews nach Nachbarschaftsgruppe und Zimmertyp
            if 'number_of_reviews' in filtered_data.columns:
                reviews_data = filtered_data.groupby(['neighbourhood_group', 'room_type'])['number_of_reviews'].sum().reset_index()
                fig_reviews = px.bar(
                    reviews_data,
                    x='neighbourhood_group',
                    y='number_of_reviews',
                    color='room_type',
                    title='Anzahl der Reviews nach Nachbarschaftsgruppe und Zimmertyp',
                    labels={'neighbourhood_group': 'Nachbarschaftsgruppe', 'number_of_reviews': 'Anzahl der Reviews', 'room_type': 'Art der Immobilie'},
                    color_discrete_sequence=[AIRBNB_COLORS['primary'], AIRBNB_COLORS['secondary'], AIRBNB_COLORS['tertiary']]
                )
                fig_reviews.update_layout(
                    plot_bgcolor='black',
                    paper_bgcolor='black',
                    font={'color': AIRBNB_COLORS['light']},
                    title_font_color=AIRBNB_COLORS['tertiary'],
                    title={
                        'text': "Anzahl der Reviews nach Nachbarschaftsgruppe und Zimmertyp",
                        'y': 0.9,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    xaxis_title_font=dict(color=AIRBNB_COLORS['dark']),
                    yaxis_title_font=dict(color=AIRBNB_COLORS['dark']),
                    xaxis=dict(tickfont=dict(color=AIRBNB_COLORS['dark'])),
                    yaxis=dict(tickfont=dict(color=AIRBNB_COLORS['dark']))
                )
                st.plotly_chart(fig_reviews, use_container_width=True)
            
            st.plotly_chart(fig_heatmap, use_container_width=True)