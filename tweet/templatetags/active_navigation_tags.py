from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, url_name):
    """
    Returns Tailwind CSS classes dynamically based on the active URL.
    """
    try:
        url = reverse(url_name)
    except NoReverseMatch:
        return ""  # Return empty string if URL resolution fails

    if context['request'].path == url:
        return "text-blue-700 font-semibold bg-gray-200 rounded-md dark:bg-gray-700 dark:text-blue-400"  # Active styles

    return "text-gray-900 hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
