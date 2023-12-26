import unittest
import havina.graph_generator as gg
import havina.filters as fs


class GraphGeneratorTest(unittest.TestCase):
    def test_worker(self):
        generator = gg.GraphGenerator(top_k=4)
        text = "Rihanna is a famous singer. She sings perfectly."
        result = generator(text, workers=1)
        expected = [
            fs.HeadTailRelations(
                head=fs.Entity(text='rihanna', wikidata_id=None),
                tail=fs.Entity(text='a famous singer', wikidata_id=None),
                relations=['be', 'sing']
            )
        ]
        self.assertEqual(result, expected)

    def test_clean_relations(self):
        input_relations = [
            fs.HeadTailRelations(
                head=fs.Entity(text='HH', wikidata_id=None),
                tail=fs.Entity(text='BB', wikidata_id=None),
                relations=['CC', 'GG', 'CC']
            ),
            fs.HeadTailRelations(
                head=fs.Entity(text='BB', wikidata_id=None),
                tail=fs.Entity(text='HH', wikidata_id=None),
                relations=['CC']
            ),
            fs.HeadTailRelations(
                head=fs.Entity(text='AA', wikidata_id='ss'),
                tail=fs.Entity(text='HH', wikidata_id='ss'),
                relations=['KK']
            ),
            fs.HeadTailRelations(
                head=fs.Entity(text='TT', wikidata_id=None),
                tail=fs.Entity(text='TT', wikidata_id=None),
                relations=['PP']
            ),
        ]
        result = gg.clean_relations(input_relations)
        expected = [
            fs.HeadTailRelations(
                head=fs.Entity(text='HH', wikidata_id=None),
                tail=fs.Entity(text='BB', wikidata_id=None),
                relations=['CC', 'GG']
            ),
            fs.HeadTailRelations(
                head=fs.Entity(text='AA', wikidata_id='ss'),
                tail=fs.Entity(text='HH', wikidata_id='ss'),
                relations=['KK']
            )
        ]
        self.assertEqual(result, expected)


if __name__ == 'main':
    unittest.main()
