from django.shortcuts import render

from rest_framework import status

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers.serializer import *

from django.contrib.auth import authenticate

from django.contrib.auth.signals import user_logged_in

from rest_framework.permissions import IsAuthenticated, AllowAny

from django.db import IntegrityError

class Login(APIView):
    """
    API View for user login. Accessible by any users.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Handle POST request for user login.
        Authenticates users and returns appropriate tokens based on user type (admin/non-admin).
        """
        try:
            # Extract username and password from request data
            username = request.data.get('username')
            password = request.data.get('password')

            # Authenticate user with provided credentials
            user = authenticate(username=username, password=password)

            if user is not None:
                # Generate token for authenticated user
                token = RefreshToken.for_user(user)

                return Response({
                    'status': True,
                    'message': 'Login successful',
                    'username': username,
                    'is_admin': user.is_superuser,
                    'refresh': str(token),
                    'access': str(token.access_token),
                }, status=status.HTTP_200_OK)
            else:
                # Authentication failed
                return Response({
                    'status': False,
                    'message': 'Invalid credentials'
                }, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        except Exception as e:
            # Handle any unexpected errors
            return Response({
                'status': False,
                'message': 'An error occurred during login',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    """
    API View for user logout. Only accessible by authenticated users.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Handle POST request for user logout. Blacklists the user's refresh token to prevent further use.
        """
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            # Blacklist the refresh token
            token.blacklist()

            return Response({
                'status': True,
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)

        except KeyError:
            # Handle missing refresh token
            return Response({
                'status': False,
                'message': 'Refresh token not provided'
            }, status=status.HTTP_206_PARTIAL_CONTENT)

        except Exception as error:
            # Handle any unexpected errors
            return Response({
                'status': False,
                'message': 'An error occurred during logout',
                'error': str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(APIView):
    """
    API View for changing user password. Accessible by any users.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Handle POST request for password change.
        Validates and updates the user's password.
        """
        try:
            # Attempt to serialize and validate password change data
            serializer = ChangePasswordSerializer(data=request.data)

            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                confirm_password = serializer.validated_data['confirm_password']

                try:
                    # Fetch the user by username
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    return Response({
                        'status': False,
                        'message': 'Invalid username'
                    }, status=status.HTTP_206_PARTIAL_CONTENT)

                # Verify password match
                if password != confirm_password:
                    return Response({
                        'status': False,
                        'message': 'Passwords do not match'
                    }, status=status.HTTP_206_PARTIAL_CONTENT)

                # Update the user's password
                user.set_password(confirm_password)
                user.save()

                return Response({
                    'status': True,
                    'message': 'Password changed successfully'
                }, status=status.HTTP_200_OK)
            else:
                # Return error if data is invalid
                return Response({
                    'status': False,
                    'message': 'Invalid data provided',
                    'errors': serializer.errors
                }, status=status.HTTP_206_PARTIAL_CONTENT)

        except Exception as e:
            # Handle any unexpected errors
            return Response({
                'status': False,
                'message': 'An error occurred while changing password',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)



class Registration(APIView):
    """
    API View for user registration. Accessible by any users.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Handle POST request for user registration.
        Creates new user account in User table only.
        """
        try:
            # Serialize and validate User data
            user_serializer = UserSerializer(data=request.data)
            if not user_serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Invalid user data provided',
                    'errors': user_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # Save User (this also handles password hashing)
            user = user_serializer.save()

            return Response({
                'status': True,
                'message': 'User registered successfully',
                'data': {
                    'user': user_serializer.data
                }
            }, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            # Handle database integrity errors (duplicate username/email)
            return Response({
                'status': False,
                'message': 'User with this username or email already exists',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle any unexpected errors
            return Response({
                'status': False,
                'message': 'An error occurred during registration',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)



class UserDetails(APIView):
    """
    API View for user details. Only accessible by authenticated users.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        """
        Handle GET request for user details.
        Returns user information from User table only.
        """
        try:
            # Get the user from User table using user_id (UUID primary key)
            user = User.objects.filter(id=id).first()
            if not user:
                return Response({
                    'status': False, 
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Build user data from User model fields
            data = {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'phone_number': user.phone_number,
                'user_type': user.user_type,
                'status': user.status,
                'profile_image_url': user.profile_image_url,
                'organization_id': str(user.organization_id) if user.organization_id else None,
                'subscription_details': user.subscription_details,
                'emergency_contact': user.emergency_contact,
                'created_at': user.created_at,
                'last_login': user.last_login,
                'is_active': user.is_active,
                'created_by': str(user.created_by) if user.created_by else None,
            }

            return Response({
                'status': True,
                'message': 'User details retrieved successfully',
                'data': data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any unexpected errors
            return Response({
                'status': False,
                'message': 'An error occurred while fetching user details',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
