{
    classic: {
        screen1: {
            ['!user_city_answer',
            '!explanation',
            '!user_city_answer']
        }
        screen2: {
            ['!prediction_city&&user_city_answer',
            '!explanation',
            '!prediction_city&&user_city_answer']
        }
        screen3: {
            ['prediction_city',
            'explanation',
            'explanation']
        }
    }
    recommender: {
        screen1: {
            ['!prediction_city',
            '!explanation',
            '!prediction city']
        }
        screen2: {
            ['prediction_city&&!user_city_answer',
            'explanation',
            'prediction_city&&!user_city_answer']
        }
        screen3: {
            ['user_city_answer',
            'explanation',
            'user_city_answer']
        }
    }
}

// -> App: data -> Variable, in der die jeweilige variante hinterlegt wird (score_order)
// -> env variable, deren Wert entweder "classic" oder "recommender" ist
// -> im Code: an allen Komponenten die v-if Bedingungen anpassen, indem der entsprechende Eintrag des dicts in data (score_order) aufgerufen wird