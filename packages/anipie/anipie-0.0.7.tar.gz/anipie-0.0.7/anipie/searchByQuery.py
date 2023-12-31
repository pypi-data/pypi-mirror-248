import re
import requests
from anipie.queries import ANIME_QUERY, MANGA_QUERY, ANIME_API_URL

class SearchByQuery:
    """A class used to search for an anime."""

    def __init__(self, title, type='ANIME'):
        """Initialize the class."""
        self._title = title
        self._type = type
        if self._type.upper() == 'ANIME':
            self._type = 'ANIME'
        elif self._type.upper() == 'MANGA':
            self._type = 'MANGA'
        else:
            raise ValueError("Type must be either 'ANIME' or 'MANGA'")
        self._search()

    def _search(self):
        """Perform the search for the anime."""
        variables = {
            'search': self._title,
            'type': self._type,
        }
        query = ANIME_QUERY if self._type.upper() == 'ANIME' else MANGA_QUERY
        try:
            response = requests.post(
                ANIME_API_URL, json={'query': query, 'variables': variables})
            response.raise_for_status()
            self._response = response.json()
            self._media = self._response.get('data').get('Media')
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def getRawData(self) -> dict:
        """Returns the raw JSON data from the API."""
        return self._response

    @property
    def getRomanjiName(self) -> str:
        """Returns the romanji name of the anime."""
        return self._media.get('title').get('romaji')
    
    @property
    def getEnglishName(self) -> str:
        """Returns the english name of the anime."""
        return self._media.get('title').get('english')
    
    @property
    def getStatus(self) -> str:
        """Returns the status of the anime."""
        return self._media.get('status')
    
    @property
    def getDescription(self) -> str:
        """Returns the description of the anime."""
        des = self._media.get('description')
        return re.sub(re.compile('<.*?>'), '', des)
    
    @property
    def getAnimeEpisodes(self) -> int:
        """Returns the number of episodes of the anime."""
        return self._media.get('episodes')
    
    @property
    def getCoverImageURL(self) -> str:
        """Returns the cover image of the anime."""
        return self._media.get('coverImage').get('large')
    
    @property
    def getGenres(self) -> str:
        """Returns the genres of the anime."""
        return ", ".join(self._media.get('genres'))
    
    @property
    def getSiteURL(self) -> str:
        """Returns the site url of the anime."""
        return self._media.get('siteUrl')
    
    @property
    def getStartDate(self) -> str:
        """Returns the start date of the anime."""
        esd = self._media.get('startDate')
        return str(esd.get('month')) + '/' + str(esd.get('day')) + '/' + str(esd.get('year'))
    
    @property
    def getEndDate(self) -> str:
        """Returns the end date of the anime."""
        exp = self._media.get('endDate')
        return str(exp.get('month')) + '/' + str(exp.get('day')) + '/' + str(exp.get('year'))
    
    @property
    def getAverageScore(self) -> float:
        """Returns the average score of the anime."""
        return int(self._media.get('averageScore'))/10
    
    @property
    def getSeason(self) -> str:
        """Returns the season of the anime."""
        return self._media.get('season')
    
    @property
    def getFormat(self) -> str:
        """Returns the format of the anime."""
        return self._media.get('format')
    
    @property
    def getID(self) -> int:
        """Returns the ID of the anime."""
        return self._media.get('id')

    @property
    def getChapters(self) -> int:
        """Returns the number of chapters of the manga."""
        return self._media.get('chapters')
    
    @property
    def getVolumes(self) -> int:
        """Returns the number of volumes of the manga."""
        return self._media.get('volumes')
    