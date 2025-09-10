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
    """Retrieve available exercises"""

    query = db.query(Exercise).filter(Exercise.is_active == True)

    # Filter by difficulty if specified
    if difficulty:
        query = query.filter(Exercise.difficulty == difficulty)

    # Filter by topic if specified
    if topic:
        query = query.filter(Exercise.topic == topic)

    exercises = query.all()

    # Convert to dictionary for the response
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
    """Retrieve the details of an exercise"""

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
    """Create some sample exercises (for development)"""

    # Check if exercises already exist
    existing = db.query(Exercise).first()
    if existing:
        return {"message": "Exercises already exist"}

    exercises_data = [
        {
            "title": "Basic Variables",
            "description": "Declare variables of different types and print them",
            "difficulty": "beginner",
            "topic": "variables",
            "starter_code": """public class Variables {
    public static void main(String[] args) {
        // Declare an int variable named 'age' with value 25

        // Declare a String variable named 'name' with your name

        // Print these variables with System.out.println()

    }
}""",
            "solution": """public class Variables {
    public static void main(String[] args) {
        int age = 25;
        String name = "Alice";

        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
    }
}""",
            "test_cases": [
                {"input": "", "expected_output": "Name: Alice\\nAge: 25"}
            ]
        },
        {
            "title": "Simple for loop",
            "description": "Use a for loop to print numbers from 1 to 5",
            "difficulty": "beginner",
            "topic": "loops",
            "starter_code": """public class ForLoop {
    public static void main(String[] args) {
        // Use a for loop to print numbers from 1 to 5

    }
}""",
            "solution": """public class ForLoop {
    public static void main(String[] args) {
        for (int i = 1; i <= 5; i++) {
            System.out.println("Number: " + i);
        }
    }
}""",
            "test_cases": [
                {"input": "", "expected_output": "Number: 1\\nNumber: 2\\nNumber: 3\\nNumber: 4\\nNumber: 5"}
            ]
        },
        {
            "title": "If/Else conditions",
            "description": "Create a program that checks if a number is even or odd",
            "difficulty": "beginner",
            "topic": "conditions",
            "starter_code": """public class EvenOdd {
    public static void main(String[] args) {
        int number = 7;

        // Use if/else to check if the number is even or odd
        // Print "The number X is even" or "The number X is odd"

    }
}""",
            "solution": """public class EvenOdd {
    public static void main(String[] args) {
        int number = 7;

        if (number % 2 == 0) {
            System.out.println("The number " + number + " is even");
        } else {
            System.out.println("The number " + number + " is odd");
        }
    }
}""",
            "test_cases": [
                {"input": "", "expected_output": "The number 7 is odd"}
            ]
        },
        {
            "title": "First class",
            "description": "Create a Person class with basic attributes and methods",
            "difficulty": "intermediate",
            "topic": "oop",
            "starter_code": """public class Person {
    // Declare private attributes: name (String) and age (int)

    // Create a constructor that takes name and age as parameters

    // Create getter methods for name and age

    // Create a method introduce() that prints "My name is X and I am Y years old"

    public static void main(String[] args) {
        // Create an instance of Person and test your methods

    }
}""",
            "solution": """public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }

    public void introduce() {
        System.out.println("My name is " + name + " and I am " + age + " years old");
    }

    public static void main(String[] args) {
        Person p = new Person("Alice", 25);
        p.introduce();
    }
}""",
            "test_cases": [
                {"input": "", "expected_output": "My name is Alice and I am 25 years old"}
            ]
        }
    ]

    # Create exercises in database
    for ex_data in exercises_data:
        exercise = Exercise(**ex_data)
        db.add(exercise)

    db.commit()

    return {"message": f"Created {len(exercises_data)} exercises successfully"}
