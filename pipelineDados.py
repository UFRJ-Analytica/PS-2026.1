#pipeline deserto transportes
import pandas as pd
from shapely import LineString, wkt, Point


'''Lendo todos os arquivos do GTFS (mesmo os que não usaremos, devem ser retirados mais tarde)'''
agency = pd.read_csv("agency.csv")
#'feed_version', 'feed_start_date', 'feed_end_date', 'agency_id',
# 'agency_name', 'agency_url', 'agency_timezone', 'agency_lang', 'versao_modelo'

calendar = pd.read_csv("calendar.csv")
#'feed_version', 'feed_start_date', 'feed_end_date', 'service_id',
#'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'start_date', 'end_date', 'versao_modelo'

calendarDates = pd.read_csv("calendar_dates.csv")
#'feed_version', 'feed_start_date', 'feed_end_date', 'service_id',
#'DATE', 'exception_type', 'versao_modelo'

fareAttributes = pd.read_csv("fare_attributes.csv")
#'feed_version', 'feed_start_date', 'feed_end_date', 'fare_id', 'price',
#'currency_type', 'payment_method', 'transfers', 'agency_id','transfer_duration', 'versao_modelo'

fareRules = pd.read_csv("fare_rules.csv")
#'feed_version', 'feed_start_date', 'feed_end_date', 'fare_id',
#'route_id', 'origin_id', 'destination_id', 'contains_id','versao_modelo'

feedInfo = pd.read_csv("feed_info.csv")
#'feed_version', 'feed_start_date', 'feed_end_date','feed_publisher_name', 'feed_publisher_url', 'feed_lang',
#'default_lang', 'feed_contact_email', 'feed_contact_url','feed_update_datetime', 'versao_modelo'

frequencies = pd.read_csv("frequencies.csv")
#'feed_version', 'feed_start_date', 'feed_end_date', 'trip_id', 
# 'start_time', 'end_time', 'headway_secs', 'exact_times','versao_modelo'

ordemServico = pd.read_csv("ordem_servico.csv")
#'feed_version', 'feed_start_date', 'feed_end_date', 'tipo_os', 'servico', 
# 'vista', 'consorcio', 'horario_inicio', 'horario_fim', 'extensao_ida', 'extensao_volta', 'partidas_ida', 'partidas_volta',
#'viagens_planejadas', 'distancia_total_planejada', 'tipo_dia', 'versao_modelo'

ordemServicoAlt = pd.read_csv("ordem_servico_trajeto_alternativo.csv")
#'feed_version', 'feed_start_date', 'feed_end_date', 'tipo_os', 'servico', 'consorcio', 'vista', 'ativacao', 'descricao', 'evento',
#'extensao_ida', 'extensao_volta', 'inicio_periodo', 'fim_periodo','versao_modelo'

shapesGeom = pd.read_csv("shapes_geom.csv")
#'feed_version', 'feed_start_date', 'feed_end_date', 'shape_id', 'shape',
#'shape_distance', 'start_pt', 'end_pt', 'versao_modelo'

routes = pd.read_csv("routes.csv")
#'feed_version', 'feed_start_date', 'feed_end_date', 'route_id','agency_id', 
#'route_short_name', 'route_long_name', 'route_desc','route_type', 'route_url', 'route_color', 'route_text_color',
#'route_sort_order', 'continuous_pickup', 'continuous_drop_off','network_id', 'versao_modelo'

stops = pd.read_csv("stops.csv")
#'feed_version', 'feed_start_date', 'feed_end_date', 'stop_id','stop_code', 'stop_name', 'tts_stop_name', 'stop_desc', 'stop_lat',
#'stop_lon', 'zone_id', 'stop_url', 'location_type', 'parent_station','stop_timezone', 
# 'wheelchair_boarding', 'level_id', 'platform_code', 'versao_modelo'

paradas = pd.read_csv("paradas.csv")
#'X', 'Y', 'fid', 'wheelchair_boarding', 'zone_id', 'platform_code','stop_id', 
# 'stop_code', 'stop_url', 'stop_desc', 'stop_timezone','stop_name', 'location_type', 'parent_station'

trips = pd.read_csv("trips.csv")
#'feed_version', 'feed_start_date', 'feed_end_date', 'route_id','service_id', 'trip_id', 'trip_headsign', 'trip_short_name',
#'direction_id', 'block_id', 'shape_id', 'wheelchair_accessible','bikes_allowed', 'versao_modelo'


'''Tirando colunas desnecessárias dos dados de interesse'''
routes = routes.drop(columns=['feed_version', 'feed_start_date', 
                              'feed_end_date', 'agency_id', 'route_url', 'route_color', 'route_text_color','network_id', 'versao_modelo',
                              'route_sort_order', 'continuous_pickup', 'continuous_drop_off'])


trips = trips.drop(columns=['feed_version', 'feed_start_date', 'feed_end_date',
                            'service_id','block_id', 'wheelchair_accessible','bikes_allowed', 'versao_modelo'])


stops = stops.drop(columns=['feed_version', 'feed_start_date', 'feed_end_date', 'wheelchair_boarding', 'stop_code',
                            'level_id', 'platform_code', 'versao_modelo', 'stop_timezone','tts_stop_name', 'stop_desc', 
                            'zone_id', 'stop_url', 'location_type', 'parent_station'])

shapesGeom = shapesGeom.drop(columns=['feed_version', 'feed_start_date', 'feed_end_date', 'versao_modelo'])

#Após retirar, cada um desses dataframes têm as seguintes colunas:
#trips: route_id, trip_id, trip_headsign, trip_short_name, direction_id, shape_id
#routes: route_id, route_short_name, route_long_name, route_desc, route_type
#stops: stop_id, stop_name, stop_lat, stop_lon
#shapesGeom: shape_id, shape, shape_distance, start_pt, end_pt

def quantidadeDeViagensPorRota():
    '''Conta quantas viagens são feitas por rota. Cria um dataframe (viagensRota) que possui como colunas: id da rota("route_id"), 
    quantidade de viagens("count") e nome da rota("route_long_name).'''
    quantidades = trips["route_id"].value_counts().reset_index()
    viagensRota = quantidades.merge(routes[['route_id', 'route_long_name']], on='route_id', how='left')
    return viagensRota
     


def pegarTodasParadas():
    '''Para cada shape, listar todos stops que passam por ela.'''
    todasParadas = pd.DataFrame(columns=["shape", "paradas"])
    i=0
    for linestring in shapesGeom["shape"]:
        linha = wkt.loads(linestring)
        paradas = [ ]
        for pontos in stops.itertuples():
            latitude = float(pontos[3])
            longitude = float(pontos[4])
            coordenada = Point(longitude, latitude)
            if linha.distance(coordenada)<=0.00002:
                paradas.append(pontos[2])
        todasParadas.loc[i] = [linestring, paradas]
        i+=1
    print(todasParadas)
    return todasParadas
            

        

viagensRota = quantidadeDeViagensPorRota()
print(viagensRota)

#pegarTodasParadas()


    



