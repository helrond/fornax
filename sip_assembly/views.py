import urllib
from os.path import join

from asterism.views import prepare_response
from fornax import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from sip_assembly.models import SIP
from sip_assembly.routines import (CleanupRequester, CleanupRoutine,
                                   SIPActions, SIPAssembler)
from sip_assembly.serializers import SIPListSerializer, SIPSerializer


class SIPViewSet(ModelViewSet):
    """
    retrieve:
    Return data about a SIP, identified by a primary key.

    list:
    Return paginated data about all SIPs, ordered by most recently created.

    create:
    Create a new SIP.
    """
    model = SIP
    queryset = SIP.objects.all().order_by('-created')

    def get_serializer_class(self):
        if self.action == 'list':
            return SIPListSerializer
        return SIPSerializer

    def create(self, request):
        """
        Allow for post requests from Ursa Major 0.x or 1.x
        """
        try:
            if request.data.get('bag_data'):
                sip = SIP(
                    process_status=10,
                    bag_path=join(
                        settings.BASE_DIR,
                        settings.SRC_DIR,
                        "{}.tar.gz".format(
                            request.data['identifier'])),
                    bag_identifier=request.data['identifier'],
                    # expects bag data json to be in a certain format (Ursa
                    # Major 1.x)
                    data=request.data['bag_data'],
                    # expects origin to be include in POST request (Ursa Major
                    # 1.x)
                    origin=request.data['origin']
                )
            else:
                sip = SIP(
                    process_status=10,
                    bag_path=join(
                        settings.BASE_DIR,
                        settings.SRC_DIR,
                        "{}.tar.gz".format(
                            request.data['identifier'])),
                    bag_identifier=request.data['identifier'],
                    # expects bag data json to be in a certain format (Ursa
                    # Major 0.x)
                    data=request.data
                )
            sip.save()
            return Response(prepare_response(
                ("SIP created", sip.bag_identifier)), status=200)
        except Exception as e:
            return Response(prepare_response(
                "Error creating SIP: {}".format(str(e))), status=500)


class ArchivematicaAPIView(APIView):
    """Base class for Archivematica views."""

    def post(self, request):
        try:
            response = (getattr(SIPActions(), self.method)(self.type)
                        if hasattr(self, 'type')
                        else getattr(SIPActions(), self.method)())
            return Response(prepare_response(response), status=200)
        except Exception as e:
            return Response(prepare_response(e), status=500)


class CreatePackageView(ArchivematicaAPIView):
    """Approves transfers in Archivematica. Accepts POST requests only."""
    method = 'create_package'


class RemoveCompletedTransfersView(ArchivematicaAPIView):
    """Removes completed transfers from Archivematica dashboard. Accepts POST requests only."""
    method = 'remove_completed'
    type = 'transfers'


class RemoveCompletedIngestsView(ArchivematicaAPIView):
    """Removes completed ingests from Archivematica dashboard. Accepts POST requests only."""
    method = 'remove_completed'
    type = 'ingests'


class BaseRoutineView(APIView):
    """Base view for routines. Provides a `get_args()` method which is overriden by child routines."""

    def post(self, request, format=None):
        args = self.get_args(request)
        try:
            response = self.routine(*args).run()
            return Response(prepare_response(response), status=200)
        except Exception as e:
            return Response(prepare_response(e), status=500)


class SIPAssemblyView(BaseRoutineView):
    """Runs the AssembleSIPs cron job. Accepts POST requests only."""
    routine = SIPAssembler

    def get_args(self, request):
        dirs = ({'src': settings.TEST_SRC_DIR, 'tmp': settings.TEST_TMP_DIR, 'dest': settings.TEST_DEST_DIR}
                if request.POST.get('test') else None)
        return (dirs,)


class CleanupRequestView(BaseRoutineView):
    """Sends request to previous microservice to clean up source directory."""
    routine = CleanupRequester

    def get_args(self, request):
        url = request.GET.get('post_service_url')
        data = (urllib.parse.unquote(url) if url else '')
        return (data,)


class CleanupRoutineView(BaseRoutineView):
    """Removes a transfer from the destination directory. Accepts POST requests only."""
    routine = CleanupRoutine

    def get_args(self, request):
        dirs = {
            "src": settings.TEST_SRC_DIR,
            "dest": settings.TEST_DEST_DIR} if request.POST.get('test') else None
        identifier = request.data.get('identifier')
        return (identifier, dirs)
