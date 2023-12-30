"""
Base module for the anime facts rest api. The API documentation can be found at 
https://chandan-02.github.io/anime-facts-rest-api/

Mantainer of the API: Chandan Kumar (https://github.com/chandan-02)
"""
import typing, requests, random

from anime_api import exceptions
from anime_api.apis.anime_facts_rest_api.objects import Anime, Fact


class AnimeFactsRestAPI:
    """
    Docs: https://chandan-02.github.io/anime-facts-rest-api/
    """

    endpoint = "https://anime-facts-rest-api.herokuapp.com/api/v1"

    def get_animes(self) -> typing.List[Anime]:
        """
        Returns a list of all animes.
        """
        response = requests.get(self.endpoint)

        if response.status_code != 200:
            raise exceptions.ServerError(
                status_code=response.status_code,
            )

        return [
            Anime(
                id=anime["anime_id"],
                name=anime["anime_name"],
                image=anime["anime_img"],
            )
            for anime in response.json()["data"]
        ]

    def get_anime_facts(self, anime_name: str) -> typing.List[Fact]:
        """
        Returns a list of facts about the given anime (by it's name).
        """
        response = requests.get(f"{self.endpoint}/{anime_name}")

        if response.status_code != 200:
            raise exceptions.ServerError(
                status_code=response.status_code
            )

        return [
            Fact(id=fact["fact_id"], fact=fact["fact"]) for fact in response.json()["data"]
        ]

    def get_anime_random_fact(self, anime_name: str) -> Fact:
        """
        Return a random fact about the given anime (by it's name).
        """
        return random.choice(self.get_anime_facts(anime_name))

    def get_fact(self, anime_name: str, fact_id: int) -> Fact:
        """
        Returns a specific Fact by it's ID and it's anime's name.
        """
        response = requests.get(f"{self.endpoint}/{anime_name}/{fact_id}")

        if response.status_code != 200:
            raise exceptions.ServerError(
                status_code=response.status_code,
            )

        return Fact(id=response.json()["data"]["fact_id"], fact=response.json()["data"]["fact"])
