from rest_framework.decorators import api_view
from django.http import HttpResponse
from KebbeTransit.Transit import transit
import json


@api_view(['POST'])
def path_list(request):
    if request.method == 'POST':

        #Get Info from float
        src1 = float(request.POST.get('src1'))
        src2 = float(request.POST.get('src2'))
        dest1 = float(request.POST.get('dest1'))
        dest2 = float(request.POST.get('dest2'))

        #Format info into tuples
        source = (src1, src2)
        destination = (dest1, dest2)

        #Create instance of Object
        TransitObject = transit.Transit()

        #Get Latest Data from Json
        TransitObject.getdata()

        #Get Path From Transit Algo
        path = TransitObject.findpath(source, destination)

        #return The Path as HTTP Response
        plotted_paths = TransitObject.plot_path(path)
        json_path = json.dumps(plotted_paths)
        return HttpResponse(json_path)

@api_view(['POST'])
def writetojson(request):
    if request.method == 'POST':

        #Get Info from float
        routes = request.POST.get('routes')
        crosses = request.POST.get('crosses')
        markers = request.POST.get('markers')
        # data = json.load(request.POST)
        # print data
        st=""

        print request.POST.keys()
        print markers

        return HttpResponse(routes)

