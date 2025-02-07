import sys
import os

# Add the parent directory to the sys.path to make 'models' module visible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.mema_model import MeMaArticle, Mention, Person, Author
from isagog_kg.models.logic_model import KGSerializer  # Adjust the import path as necessary


def test_instantiation():
    
    serializer = KGSerializer()
    
    author = Author(
        name = "Matteo",
        surname = "Bartocci")
    
    article = MeMaArticle(
    directus_id = "kjahfk8297ihkfjhwyriq",
    title = "Forza Roma!",
    authored_by = [author],
    published_day = "2021-01-01",)
 
    
    entity = Person(    
    name = "Prosdocimo",
    surname = "Trombetti")
    
    
    mention = Mention(    
    referent = [entity])
    
    article.yields = [mention]   
    
    
    print(serializer.serialize(article))
    
    
    
    


if __name__ == '__main__':
    

    test_instantiation()