from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
 
from api.mixins import MultipartParserMixin, ReorderMixin, VisibilityMixin
from api.permissions import IsAdminOrReadOnly

from flats.models import Flat
from flats.serializers import FlatListSerializer
from plots.models import Plot
from plots.serializers import PlotListSerializer 
from projects.models import Project
from projects.serializers import ProjectListSerializer
from testimonials.models import Testimonial
from testimonials.serializers import TestimonialSerializer
from contact.models import SiteSettings
from contact.serializers import SiteSettingsBriefSerializer
 
from home.models import HeroSlide, HomeSection
from home.serializers import HeroSlideSerializer, HomeSectionSerializer
from partners.models import Partner
from partners.serializers import PartnerSerializer
 
 
class HeroSlideViewSet(ReorderMixin, MultipartParserMixin, VisibilityMixin, viewsets.ModelViewSet):
    """
    Visitor: GET list / detail (active slides, in order).
    Admin:   full CRUD (multipart) + POST /reorder/ with {"ids": [...]}.
    """
 
    queryset = HeroSlide.objects.all()
    serializer_class = HeroSlideSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    filterset_fields = ["is_active"]
    ordering_fields = ["order", "created_at"]
 
 
class HomeSectionViewSet(MultipartParserMixin, VisibilityMixin, viewsets.ModelViewSet):
    """Visitor: read active sections. Admin: full CRUD. Detail URL uses the key."""
 
    queryset = HomeSection.objects.all()
    serializer_class = HomeSectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    lookup_field = "key"
    filterset_fields = ["key", "is_active"]
 
 
class HomeAPIView(APIView):
    """
    One call for the whole home page (public, active content only):
    slides, sections, featured projects / plots / flats, testimonials, partners
    and the site settings (without the long legal texts).
    """
 
    permission_classes = [AllowAny]
 
    def get(self, request):
        context = {"request": request}
        slides = HeroSlide.objects.filter(is_active=True)
        sections = HomeSection.objects.filter(is_active=True)
        featured_projects = Project.objects.filter(is_active=True, is_featured=True).select_related(
            "category"
        )[:3]
        featured_plots = Plot.objects.filter(is_active=True, is_featured=True).select_related(
            "project"
        )[:3]
        featured_flats = Flat.objects.filter(is_active=True, is_featured=True).select_related(
            "project"
        )[:3]
        testimonials = Testimonial.objects.filter(is_active=True)[:10]
        partners = Partner.objects.filter(is_active=True)[:24]
        site_settings = SiteSettings.load()
        return Response(
            {
                "slides": HeroSlideSerializer(slides, many=True, context=context).data,
                "featured_projects": ProjectListSerializer(
                    featured_projects, many=True, context=context
                ).data,
                "featured_plots": PlotListSerializer(featured_plots, many=True, context=context).data,
                "featured_flats": FlatListSerializer(featured_flats, many=True, context=context).data,
                "testimonials": TestimonialSerializer(testimonials, many=True, context=context).data,
                "partners": PartnerSerializer(partners, many=True, context=context).data,
                "site_settings": SiteSettingsBriefSerializer(site_settings, context=context).data,
                "sections": {
                    section.key: HomeSectionSerializer(section, context=context).data
                    for section in sections
                },
            }
        )
 
 