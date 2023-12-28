from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import AnonRateThrottle

import jwt, math
from datetime import datetime

from movie_page.settings import SECRET_KEY

from blog.models import Movie, AccessTokensBlackList
from blog.serializers import UserSerializer, MovieSerializer, TokenSerializer
from blog.variables import DEVICE_DECORATORS
from blog.decorators import device_crud




# view for registering users
class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            movies = Movie.objects.filter(id=pk)
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MovieView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            all_data = Movie.objects.all().order_by("-id")
            
            page_counts = math.ceil(all_data.count() / 8.0)
            paginator = Paginator(all_data, 8)

            # Get the current page number from the request (default to 1)
            page_number = request.GET.get('page', 1)

            try:
                page_obj = paginator.page(page_number)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage as e:
                return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

            # Serialize the current page's data
            serializer = MovieSerializer(page_obj, many=True)
            return Response({ "data" : serializer.data, "total_pages":page_counts})
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            movie = Movie.objects.create(title = request.data["title"],
                                        release_year = request.data["release_year"],
                                        image = request.FILES["image"])
            movie.save()
            serializer = MovieSerializer(movie)
            return Response({ "message":"Movie added successfully.", "data":serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            try:
                movie = Movie.objects.filter(pk=pk).first()
            except Movie.DoesNotExist:
                return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
            
            movie.image = request.FILES["image"] if "image" in request.FILES else movie.image
            
            serializer = MovieSerializer(movie, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({"message":"Movie updated successfully.", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        to log the user out.
        we are blacklisting the refresh token and access token from the header.
        """
        try:
            token = RefreshToken(request.data.get('refresh'))
            access_token = request.META.get('HTTP_AUTHORIZATION', None).split()[1]
            decoded_data = jwt.decode(access_token,key=SECRET_KEY, algorithms=['HS256'])
            jti = decoded_data['jti']
            expiry = datetime.fromtimestamp(decoded_data['exp'])

            try:
                AccessTokensBlackList.objects.create(
                    jti = jti,
                    user = request.user,
                    expires_at = expiry,
                    token = access_token
                )
                RefreshToken(token).blacklist()
            except:
                pass
            return Response({"message": "Logged out successfully."}, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': "Token is invalid or expired"}, status = status.HTTP_403_FORBIDDEN)


class UserTokenObtainView(TokenObtainPairView):
    throttle_classes = AnonRateThrottle,
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        try:
            data = {}
            data = super(UserTokenObtainView, self).post(request, *args, *kwargs)
            data = data.__dict__["data"]
            data.update({"message":"Log in successful"},status=status.HTTP_200_OK)
            return Response(data)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)