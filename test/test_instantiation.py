import sys
import os

# Add the parent directory to the sys.path to make 'models' module visible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.mema_model import MeMaArticle, Mention, Person


def test_instantiation():
    article = MeMaArticle(
    directus_id = "kjahfk8297ihkfjhwyriq",
    title = "Test Title",
    author = "Test Author",
    published_day = "2021-01-01",)
 
    
    entity = Person(    
    name = "Prosdocimo",
    surname = "Trombetti")
    
    
    mention = Mention(    
    referent = [entity])
    
    article.yields = [mention]
    
    print(article.triples())
    
    
    
    


if __name__ == '__main__':
    

    test_instantiation()