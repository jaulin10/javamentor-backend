from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.routers.auth import get_current_user
from app.schemas.user import UserResponse
from app.models.exercise import Exercise

router = APIRouter()


@router.get("/", response_model=List[dict])
def get_exercises(
        difficulty: str = None,
        topic: str = None,
        current_user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Récupérer les exercices disponibles"""

    query = db.query(Exercise).filter(Exercise.is_active == True)

    # Filtrer par difficulté si spécifiée
    if difficulty:
        query = query.filter(Exercise.difficulty == difficulty)

    # Filtrer par sujet si spécifié
    if topic:
        query = query.filter(Exercise.topic == topic)

    exercises = query.all()

    # Convertir en dictionnaire pour la réponse
    return [
        {
            "id": ex.id,
            "title": ex.title,
            "description": ex.description,
            "difficulty": ex.difficulty,
            "topic": ex.topic,
            "starter_code": ex.starter_code
        }
        for ex in exercises
    ]


@router.get("/{exercise_id}")
def get_exercise_details(
        exercise_id: int,
        current_user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Récupérer les détails d'un exercice"""

    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.is_active == True
    ).first()

    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found"
        )

    return {
        "id": exercise.id,
        "title": exercise.title,
        "description": exercise.description,
        "difficulty": exercise.difficulty,
        "topic": exercise.topic,
        "starter_code": exercise.starter_code,
        "test_cases": exercise.test_cases
    }


@router.post("/seed")
def seed_exercises(
        current_user: UserResponse = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Créer quelques exercices d'exemple (pour le développement)"""

    # Vérifier s'il y a déjà des exercices
    existing = db.query(Exercise).first()
    if existing:
        return {"message": "Exercises already exist"}

    exercises_data = [
        {
            "title": "Variables de base",
            "description": "Déclarez des variables de différents types et affichez-les",
            "difficulty": "beginner",
            "topic": "variables",
            "starter_code": """public class Variables {
    public static void main(String[] args) {
        // Déclarez une variable int nommée 'age' avec la valeur 25

        // Déclarez une variable String nommée 'nom' avec votre nom

        // Affichez ces variables avec System.out.println()

    }
}""",
            "solution": """public class Variables {
    public static void main(String[] args) {
        int age = 25;
        String nom = "Alice";

        System.out.println("Nom: " + nom);
        System.out.println("Age: " + age);
    }
}""",
            "test_cases": [
                {"input": "", "expected_output": "Nom: Alice\\nAge: 25"}
            ]
        },
        {
            "title": "Boucle for simple",
            "description": "Utilisez une boucle for pour afficher les nombres de 1 à 5",
            "difficulty": "beginner",
            "topic": "loops",
            "starter_code": """public class BoucleFor {
    public static void main(String[] args) {
        // Utilisez une boucle for pour afficher les nombres de 1 à 5

    }
}""",
            "solution": """public class BoucleFor {
    public static void main(String[] args) {
        for (int i = 1; i <= 5; i++) {
            System.out.println("Nombre: " + i);
        }
    }
}""",
            "test_cases": [
                {"input": "", "expected_output": "Nombre: 1\\nNombre: 2\\nNombre: 3\\nNombre: 4\\nNombre: 5"}
            ]
        },
        {
            "title": "Conditions if/else",
            "description": "Créez un programme qui vérifie si un nombre est pair ou impair",
            "difficulty": "beginner",
            "topic": "conditions",
            "starter_code": """public class PairImpair {
    public static void main(String[] args) {
        int nombre = 7;

        // Utilisez if/else pour vérifier si le nombre est pair ou impair
        // Affichez "Le nombre X est pair" ou "Le nombre X est impair"

    }
}""",
            "solution": """public class PairImpair {
    public static void main(String[] args) {
        int nombre = 7;

        if (nombre % 2 == 0) {
            System.out.println("Le nombre " + nombre + " est pair");
        } else {
            System.out.println("Le nombre " + nombre + " est impair");
        }
    }
}""",
            "test_cases": [
                {"input": "", "expected_output": "Le nombre 7 est impair"}
            ]
        },
        {
            "title": "Première classe",
            "description": "Créez une classe Personne avec des attributs et méthodes de base",
            "difficulty": "intermediate",
            "topic": "oop",
            "starter_code": """public class Personne {
    // Déclarez des attributs privés : nom (String) et age (int)

    // Créez un constructeur qui prend nom et age en paramètres

    // Créez des méthodes getter pour nom et age

    // Créez une méthode sePresenter() qui affiche "Je m'appelle X et j'ai Y ans"

    public static void main(String[] args) {
        // Créez une instance de Personne et testez vos méthodes

    }
}""",
            "solution": """public class Personne {
    private String nom;
    private int age;

    public Personne(String nom, int age) {
        this.nom = nom;
        this.age = age;
    }

    public String getNom() {
        return nom;
    }

    public int getAge() {
        return age;
    }

    public void sePresenter() {
        System.out.println("Je m'appelle " + nom + " et j'ai " + age + " ans");
    }

    public static void main(String[] args) {
        Personne p = new Personne("Alice", 25);
        p.sePresenter();
    }
}""",
            "test_cases": [
                {"input": "", "expected_output": "Je m'appelle Alice et j'ai 25 ans"}
            ]
        }
    ]

    # Créer les exercices en base
    for ex_data in exercises_data:
        exercise = Exercise(**ex_data)
        db.add(exercise)

    db.commit()

    return {"message": f"Created {len(exercises_data)} exercises successfully"}