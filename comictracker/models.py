from django.db import models
from django.contrib.auth.models import User


class SeriesManager(models.Manager):
    def create_series(self, data):
        name = data[0]
        year = data[1]
        cgid = data[2]
        image = data[3]
        series = self.create(name=name, year=year, cgid=cgid, image=image)
        return series


class ComicManager(models.Manager):
    def create_comic(self, data, user, series):
        name = data["name"]
        number = data["number"]
        image = data["image"]
        comic_geeks_code = data["comic_geeks_code"]
        if "artist" in data.keys():
            variant = True
            artist = data["artist"]
        else:
            variant = False
            artist = None

        comic = self.create(name=name, number=number, image=image, comic_geeks_code=comic_geeks_code,
                            variant=variant, arc="", series=series, artist=artist)

        comic.users.add(user)
        comic.save()
        return comic


class ArtistManager(models.Manager):
    def create_cover(self, name):
        cover = self.create(name=name)
        return cover


class WishlistManager(models.Manager):
    def create_item(self, comickey, userkey):
        item = self.create(comic_key_id=comickey, user_key_id=userkey)
        return item


class Series(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    cgid = models.IntegerField(blank=False, default=0)
    name = models.CharField(max_length=150)
    year = models.IntegerField()
    image = models.URLField(max_length=300, null=True)

    objects = SeriesManager()

    def __str__(self):
        return str(self.id) + " : " + self.name


class Artist(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=150)

    objects = ArtistManager()

    def __str__(self):
        return self.name


class Comic(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=150)
    number = models.IntegerField(default=1000)
    comic_geeks_code = models.IntegerField(blank=False)
    arc = models.CharField(max_length=100, null=True)
    image = models.URLField(max_length=300)
    variant = models.BooleanField(default=False)

    # relationships
    users = models.ManyToManyField(User)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True)

    objects = ComicManager()

    def __str__(self):
        return str(self.id) + " : " + self.name


class Wishlist(models.Model):
    user_key = models.ForeignKey(User, on_delete=models.CASCADE)
    comic_key = models.ForeignKey(Comic, on_delete=models.CASCADE)

    objects = WishlistManager()
