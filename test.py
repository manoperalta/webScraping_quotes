import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from extracao import scanPage, findAutor, findTags


class TestScraperFunctions(unittest.TestCase):

    @patch("extracao.requests.get")           
    @patch("extracao.screenShot")             
    def test_scanPage(self, mock_screenshot, mock_requests_get):
        
        html = '''
        <div class="quote">
            <span class="text">"Teste de citação"</span>
            <small class="author">Autor Teste</small>
            <a class="tag">love</a>
            <a class="tag">life</a>
            <a class="tag">books</a>
        </div>
        <li class="next"><a href="/page/2/"></a></li>
        '''

        
        mock_response = MagicMock(status_code=200, text=html, reason="OK")
        mock_requests_get.return_value = mock_response  

        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            scanPage("http://quotes.toscrape.com", max_paginas=1)  
            
            self.assertIn("Citação: \"Teste de citação\"", fake_out.getvalue())


    @patch("extracao.requests.get")
    @patch("extracao.screenShot")
    def test_findAutor(self, mock_screenshot, mock_requests_get):
        html = '''
        <div class="quote">
            <span class="text">"Citação do autor"</span>
            <small class="author">Autor Teste</small>
            <a class="tag">sabedoria</a>
        </div>
        '''
        
        mock_response = MagicMock(status_code=200, text=html, reason="OK")
        mock_requests_get.return_value = mock_response

        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            findAutor("http://quotes.toscrape.com", autor_busca="Autor Teste")  
            self.assertIn("Autor: Autor Teste", fake_out.getvalue())  

   
    @patch("extracao.requests.get")
    @patch("extracao.screenShot")
    def test_findTags(self, mock_screenshot, mock_requests_get):
        html = '''
        <div class="quote">
            <span class="text">"Citação com humor"</span>
            <small class="author">Autor Desconhecido</small>
            <a class="tag">humor</a>
        </div>
        '''
        mock_response = MagicMock(status_code=200, text=html, reason="OK")
        mock_requests_get.return_value = mock_response

     
        with patch('sys.stdout', new=StringIO()) as fake_out:
            findTags("http://quotes.toscrape.com", tag_busca="humor")
            self.assertIn("Tags: humor", fake_out.getvalue())  


if __name__ == "__main__":
    unittest.main()
