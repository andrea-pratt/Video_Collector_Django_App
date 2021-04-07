from urllib import parse
from django.db import models
from django.core.exceptions import ValidationError


class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True)
    video_id = models.CharField(max_length=40, unique=True)


    # Used to extract the video ID from the end of the video url before saving
    def save(self, *args, **kwargs):
        try:    # If valid url, parse for url components
            url_components = parse.urlparse(self.url)
            
            # Conditional statements to check the url against standard YouTube url pattern
            if url_components.scheme != 'https':  
                raise ValidationError(f'Not a YouTube URL {self.url}')

            if url_components.netloc != 'www.youtube.com':   
                raise ValidationError(f'Not a YouTube URL {self.url}')
                
            if url_components.path != '/watch':
                raise ValidationError(f'Not a YouTube URL {self.url}')
            
            query_string = url_components.query
            if not query_string: # If the url is an empty string, raise an error
                raise ValidationError(f'Invalid YouTube URL {self.url}')
            parameters = parse.parse_qs(query_string, strict_parsing=True)
            parameter_list = parameters.get('v')
            if not parameter_list:   
                raise ValidationError(f'Invalid YouTube URL parameters {self.url}')
            self.video_id = parameter_list[0] # Extract the video id from the first (and typically only) item in the list
        except ValueError as e:  # If any of the url parsing statements fail, raise a generic error 
            raise ValidationError(f'Unable to parse URL {self.url}') from e

        # Call the default Django save function to save the modified video to the database
        super().save(*args, **kwargs)  


    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Video ID: {self.video_id},Notes: {self.notes[:200]}'
