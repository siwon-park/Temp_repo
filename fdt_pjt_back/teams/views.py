from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import *
from .serializers.team import *

User = get_user_model()

# 전체 팀 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def team_list(request):
    team_list = Team.objects.all()
    serializer = MyTeamSerializer(team_list, many=True)
    return Response(serializer.data)

# 개별 팀 조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def team_pick(request, team_pk):
    team_pick = get_object_or_404(Team, pk=team_pk)
    serializer = MyTeamSerializer(team_pick)
    return Response(serializer.data)


# 팀 페이지 조회 및 수정 및 팀장 등록 및 해제
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def myteam(request, team_pk):

    def myteam_get():
        team = get_object_or_404(Team, pk=team_pk)
        serializer = MyTeamSerializer(team)
        return Response(serializer.data)
    
    def myteam_put():
        team = get_object_or_404(Team, pk=team_pk)
        teamID = team.id
        if request.user.my_team_id == teamID:
            serializer = MyTeamSerializer(instance=team, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                serializer = MyTeamSerializer(team)
                return Response(serializer.data)
    
    if request.method == 'GET':
        return myteam_get()
    elif request.method == 'PUT':
        return myteam_put()
