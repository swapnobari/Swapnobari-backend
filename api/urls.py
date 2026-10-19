from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (
    ChangePasswordView,
    LoginView,
    LogoutView,
    ProfileView,
)

from testimonials.views import TestimonialViewSet
from news.views import NewsPostViewSet
from careers.views import JobPostViewSet, JobApplicationViewSet
from csr.views import CSRActivityViewSet
from banners.views import BannerViewSet
from home.views import HeroSlideViewSet, HomeSectionViewSet, HomeAPIView
from about.views import AboutPageView, FoundersMessageView, MissionVisionViewSet, CoreValueViewSet
from team.views import TeamMemberViewSet
from projects.views import ProjectCategoryViewSet, ProjectViewSet
from plots.views import PlotViewSet
from flats.views import FlatViewSet
from bookings.views import BookingViewSet
from landowner.views import (
    LandownerPageView,
    LandownerBenefitViewSet,
    LandownerStepViewSet,
    LandShareRequestViewSet,
)
from partners.views import PartnerViewSet
from contact.views import SiteSettingsView, ContactMessageViewSet
from footer.views import (
    FooterView,
    FooterSocialLinkViewSet,
    FooterLinkGroupViewSet,
    FooterLinkViewSet,
)


router = routers.DefaultRouter()

router.register("banners", BannerViewSet, basename = "banners")
router.register("hero-slides", HeroSlideViewSet, basename="hero-slides")
router.register("home-sections", HomeSectionViewSet, basename = "home-sections")
router.register("about/mission-vision", MissionVisionViewSet, basename="about-mission-vision")
router.register("about/values", CoreValueViewSet, basename="about-value")
router.register("teams", TeamMemberViewSet, basename="teams")
router.register("projects-categories", ProjectCategoryViewSet, basename="projects-categories")
router.register("projects", ProjectViewSet, basename = "projects")
router.register("plots", PlotViewSet, basename="plots")
router.register("flats", FlatViewSet, basename="flats")
router.register("landowner/benefits", LandownerBenefitViewSet, basename="landowner-benefits")
router.register("landowner/steps", LandownerStepViewSet, basename="landowner-steps")
router.register("landowner/requests", LandShareRequestViewSet, basename="landowner-requests")
router.register("bookings", BookingViewSet, basename="bookings")
router.register("csr", CSRActivityViewSet, basename="csr")
router.register("careers/applications", JobApplicationViewSet, basename="careers-applications")
router.register("careers", JobPostViewSet, basename="careers")
router.register("news", NewsPostViewSet, basename="news")
router.register("testimonials", TestimonialViewSet, basename="testimonials")
router.register("partners", PartnerViewSet, basename="partners")
router.register("contact", ContactMessageViewSet, basename="contact")
router.register("footer/social-links", FooterSocialLinkViewSet, basename="footer-social-links")
router.register("footer/link-groups", FooterLinkGroupViewSet, basename="footer-link-groups")
router.register("footer/links", FooterLinkViewSet, basename="footer-links")


urlpatterns = [
    path('', include(router.urls)),
    
    path("home/", HomeAPIView.as_view(), name="home-api"),
    
    path("about/", AboutPageView.as_view(), name="about"),
    path("about/founders-message/", FoundersMessageView.as_view(), name="about-founders-message"),
    
    path("landowner/page/", LandownerPageView.as_view(), name="landowner-page"),
    
    path("contact/settings/", SiteSettingsView.as_view(), name="contact-settings"),
    
    path("footer/", FooterView.as_view(), name="footer"),
    
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
    path("auth/logout/", LogoutView.as_view(), name="auth-logout"),
    path("auth/profile/", ProfileView.as_view(), name="auth-profile"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="auth-change-password"),
    
    # path('auth/', include('users.urls')),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),
]