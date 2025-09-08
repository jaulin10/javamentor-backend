import openai
import os
from typing import List, Dict
from dotenv import load_dotenv
import random

load_dotenv()

# OpenAI Configuration
openai.api_key = os.getenv("OPENAI_API_KEY")

# System prompts for different levels
SYSTEM_PROMPTS = {
    "beginner": """You are JavaMentor, an assistant specialized in Java learning for beginners.

Your objectives:
- Explain Java concepts in a simple and clear way
- Propose exercises adapted to beginner level (variables, loops, conditions)
- Correct code and give constructive advice
- Be encouraging and patient

Focus on: variables, data types, loops (for, while), conditions (if/else), simple methods.

Always respond in English and remain supportive.""",

    "intermediate": """You are JavaMentor, an assistant specialized in Java learning for intermediate level.

Your objectives:
- Explain object-oriented programming (classes, objects, inheritance)
- Propose exercises on collections (ArrayList, HashMap)
- Help with error handling (try/catch)
- Introduce advanced concepts progressively

Focus on: OOP, encapsulation, inheritance, polymorphism, collections, exceptions.

Always respond in English and adapt your level to the context.""",

    "advanced": """You are JavaMentor, an assistant specialized in Java learning for advanced level.

Your objectives:
- Explain advanced concepts (streams, lambda, generics)
- Propose exercises on design patterns
- Help with performance and optimization
- Prepare for technical interviews

Focus on: streams, lambda, generics, multithreading, design patterns, frameworks.

Always respond in English with a high technical level."""
}


class OpenAIService:
    def __init__(self):
        if not openai.api_key:
            raise ValueError("OpenAI API key not set")
        # self.client = openai.OpenAI() if openai.api_key else None

    def is_available(self) -> bool:
        """Check if OpenAI is configured"""
        return openai.api_key is not None and openai.api_key != "sk-fake-key-for-now"

    def generate_response(self, message: str, user_level: str = "beginner",
                          conversation_history: List[Dict] = None) -> str:
        """Generate a response with OpenAI"""

        if not self.is_available():
            return self._fallback_response(message, user_level)

        try:
            # Build conversation history
            messages = [{"role": "system", "content": SYSTEM_PROMPTS.get(user_level, SYSTEM_PROMPTS["beginner"])}]

            # Add history (max 10 last messages)
            if conversation_history:
                for msg in conversation_history[-10:]:
                    role = "assistant" if msg.get("is_bot") else "user"
                    messages.append({"role": role, "content": msg.get("content", "")})

            # Add current message
            messages.append({"role": "user", "content": message})

            # Call to OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"OpenAI Error: {e}")
            return self._fallback_response(message, user_level)

    def _fallback_response(self, message: str, user_level: str) -> str:
        """Enhanced fallback responses with intelligent keyword detection"""

        message_lower = message.lower()

        # Variables and data types - Enhanced detection
        if any(word in message_lower for word in
               ["variable", "int", "string", "double", "boolean", "declaration", "declare", "data type", "primitive"]):
            return self._get_variables_response(user_level)

        # Loops - Enhanced detection
        elif any(word in message_lower for word in
                 ["loop", "for", "while", "iteration", "repeat", "do-while", "enhanced for", "foreach"]):
            return self._get_loops_response(user_level)

        # Classes and OOP - Enhanced detection
        elif any(word in message_lower for word in
                 ["class", "object", "oop", "method", "constructor", "inheritance", "encapsulation", "polymorphism",
                  "abstraction"]):
            return self._get_oop_response(user_level)

        # Collections and arrays - New category
        elif any(word in message_lower for word in
                 ["array", "arraylist", "list", "collection", "hashmap", "set", "map", "iterator"]):
            return self._get_collections_response(user_level)

        # Conditions - Enhanced detection
        elif any(word in message_lower for word in
                 ["if", "else", "condition", "switch", "case", "ternary", "conditional"]):
            return self._get_conditions_response(user_level)

        # Error handling - New category
        elif any(word in message_lower for word in
                 ["error", "exception", "try", "catch", "finally", "throw", "throws", "debug"]):
            return self._get_error_handling_response(user_level)

        # Input/Output - New category
        elif any(word in message_lower for word in
                 ["input", "output", "scanner", "print", "println", "file", "read", "write"]):
            return self._get_io_response(user_level)

        # Exercises and practice
        elif any(word in message_lower for word in
                 ["exercise", "practice", "training", "challenge", "homework", "project"]):
            return self._get_exercise_response(user_level)

        # Greetings and help
        elif any(word in message_lower for word in ["help", "hello", "hi", "start", "begin", "what can you do"]):
            return self._get_help_response(user_level)

        # Default response
        else:
            return self._get_default_response(message, user_level)

    def _get_variables_response(self, user_level: str) -> str:
        """Enhanced variable explanations by level"""
        if user_level == "beginner":
            return """In Java, variables store data. Here's the basic syntax:

```java
dataType variableName = value;
```

**Primitive data types:**
```java
int age = 25;           // Whole numbers (-2,147,483,648 to 2,147,483,647)
double price = 19.99;   // Decimal numbers (64-bit floating point)
boolean isActive = true; // True or false values
char grade = 'A';       // Single character (16-bit Unicode)
long bigNumber = 1000000L; // Large whole numbers
float temperature = 98.6f; // 32-bit floating point
```

**Reference types:**
```java
String name = "Alice";  // Text (object, not primitive)
```

**Variable naming rules:**
- Start with letter, underscore, or $
- Use camelCase (firstName, not first_name)
- Cannot use Java keywords (int, class, etc.)

Would you like me to propose an exercise on variables?"""

        elif user_level == "intermediate":
            return """Variables in Java have different scopes and access levels:

**Variable types by scope:**
```java
public class Example {
    static int classVariable = 100;     // Shared by all instances
    private int instanceVariable = 50;  // Unique to each object

    public void method() {
        int localVariable = 10;         // Only exists in this method
        final int CONSTANT = 5;         // Cannot be changed
    }
}
```

**Access modifiers:**
```java
public int publicVar;    // Accessible from anywhere
private int privateVar;  // Only within this class
protected int protectedVar; // Within package + subclasses
int packageVar;          // Within package only (default)
```

**Best practices:**
- Use meaningful names (accountBalance vs bal)
- Make fields private, provide public getters/setters
- Use final for constants (static final for class constants)
- Initialize variables before use

What aspect of variable scope interests you?"""

        else:  # advanced
            return """Advanced variable concepts in Java:

**Generic variables and type safety:**
```java
List<String> names = new ArrayList<>();
Map<Integer, User> userMap = new HashMap<>();
Optional<String> result = Optional.empty();
```

**Functional interfaces and lambda variables:**
```java
Function<String, Integer> stringLength = String::length;
Predicate<Integer> isEven = num -> num % 2 == 0;
Consumer<String> printer = System.out::println;
```

**Variable capture in lambdas (effectively final):**
```java
int multiplier = 10; // Must be effectively final
List<Integer> numbers = Arrays.asList(1, 2, 3);
numbers.stream()
       .map(n -> n * multiplier)
       .forEach(System.out::println);
```

**Volatile and thread safety:**
```java
private volatile boolean running = true; // Ensures visibility across threads
```

Which advanced concept would you like to explore?"""

    def _get_loops_response(self, user_level: str) -> str:
        """Enhanced loop explanations by level"""
        if user_level == "beginner":
            return """Loops repeat code multiple times. Java has several types:

**1. For loop (when you know iteration count):**
```java
for (int i = 0; i < 5; i++) {
    System.out.println("Count: " + i);
}
// Output: Count: 0, Count: 1, Count: 2, Count: 3, Count: 4
```

**2. While loop (condition-based):**
```java
int count = 0;
while (count < 5) {
    System.out.println("Count: " + count);
    count++; // Don't forget to increment!
}
```

**3. Enhanced for loop (for arrays/collections):**
```java
int[] numbers = {1, 2, 3, 4, 5};
for (int number : numbers) {
    System.out.println("Number: " + number);
}
```

**4. Do-while loop (executes at least once):**
```java
int input;
do {
    input = scanner.nextInt();
    System.out.println("You entered: " + input);
} while (input != 0);
```

Which type of loop would you like to practice?"""

        elif user_level == "intermediate":
            return """Advanced loop patterns and control:

**Nested loops for 2D operations:**
```java
int[][] matrix = {{1,2,3}, {4,5,6}, {7,8,9}};
for (int i = 0; i < matrix.length; i++) {
    for (int j = 0; j < matrix[i].length; j++) {
        System.out.print(matrix[i][j] + " ");
    }
    System.out.println();
}
```

**Loop control statements:**
```java
for (int i = 0; i < 10; i++) {
    if (i == 3) continue;    // Skip this iteration
    if (i == 7) break;       // Exit loop completely
    System.out.println(i);   // Prints: 0,1,2,4,5,6
}
```

**Iterating collections with enhanced features:**
```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

// Traditional enhanced for
for (String name : names) {
    System.out.println(name.toUpperCase());
}

// With index using traditional for
for (int i = 0; i < names.size(); i++) {
    System.out.println(i + ": " + names.get(i));
}
```

What specific loop pattern are you working with?"""

        else:  # advanced
            return """Modern iteration patterns and performance optimization:

**Stream API (functional approach):**
```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// Traditional loop equivalent
numbers.stream()
       .filter(n -> n % 2 == 0)
       .map(n -> n * n)
       .forEach(System.out::println);

// Parallel processing for large datasets
numbers.parallelStream()
       .filter(this::isPrime)
       .collect(Collectors.toList());
```

**Custom iterators and Iterable:**
```java
public class Range implements Iterable<Integer> {
    private final int start, end;

    public Range(int start, int end) {
        this.start = start; this.end = end;
    }

    @Override
    public Iterator<Integer> iterator() {
        return new Iterator<Integer>() {
            private int current = start;

            @Override
            public boolean hasNext() { return current < end; }

            @Override
            public Integer next() {
                if (!hasNext()) throw new NoSuchElementException();
                return current++;
            }
        };
    }
}

// Usage: for (int i : new Range(1, 11)) { ... }
```

**Performance considerations:**
- Use enhanced for with collections (cleaner, less error-prone)
- Consider parallel streams for CPU-intensive operations on large datasets
- Avoid object creation in tight loops

Interested in functional programming patterns or performance optimization?"""

    def _get_oop_response(self, user_level: str) -> str:
        """Enhanced OOP explanations by level"""
        if user_level == "beginner":
            return """A class is a blueprint for creating objects. Think of it like a cookie cutter:

```java
public class Dog {
    // Attributes (what the dog has)
    private String name;
    private String breed;
    private int age;

    // Constructor (how to create a dog)
    public Dog(String name, String breed, int age) {
        this.name = name;
        this.breed = breed;
        this.age = age;
    }

    // Methods (what the dog can do)
    public void bark() {
        System.out.println(name + " says Woof!");
    }

    public void celebrate() {
        System.out.println(name + " is wagging tail!");
    }

    // Getters (to access private attributes)
    public String getName() { return name; }
    public String getBreed() { return breed; }
    public int getAge() { return age; }
}
```

**Using the class:**
```java
Dog myDog = new Dog("Buddy", "Golden Retriever", 3);
myDog.bark();      // Output: Buddy says Woof!
myDog.celebrate(); // Output: Buddy is wagging tail!
System.out.println("My dog " + myDog.getName() + " is " + myDog.getAge() + " years old");
```

Try creating a simple Person class with name, age, and a greet() method!"""

        elif user_level == "intermediate":
            return """Object-oriented programming has four fundamental principles:

**1. Encapsulation (data hiding and protection):**
```java
public class BankAccount {
    private double balance; // Private = cannot be accessed directly
    private String accountNumber;

    public BankAccount(String accountNumber, double initialBalance) {
        this.accountNumber = accountNumber;
        this.balance = initialBalance;
    }

    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println("Deposited: $" + amount);
        }
    }

    public boolean withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            return true;
        }
        return false;
    }

    public double getBalance() { return balance; } // Controlled access
}
```

**2. Inheritance (code reuse and "is-a" relationships):**
```java
public class Animal {
    protected String name;
    protected int age;

    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public void eat() {
        System.out.println(name + " is eating");
    }
}

public class Cat extends Animal {
    private String furColor;

    public Cat(String name, int age, String furColor) {
        super(name, age); // Call parent constructor
        this.furColor = furColor;
    }

    public void meow() {
        System.out.println(name + " says Meow!");
    }

    @Override
    public void eat() {
        System.out.println(name + " is eating cat food");
    }
}
```

**3. Polymorphism (one interface, many forms):**
```java
Animal pet1 = new Cat("Whiskers", 2, "Orange");
Animal pet2 = new Dog("Rex", 4, "Labrador");

pet1.eat(); // Calls Cat's version: "Whiskers is eating cat food"
pet2.eat(); // Calls Dog's version (if overridden)
```

Which OOP principle would you like to explore further?"""

        else:  # advanced
            return """Advanced OOP patterns and modern Java features:

**Abstract classes and interfaces with default methods:**
```java
public abstract class Shape {
    protected String color;

    public Shape(String color) { this.color = color; }

    public abstract double calculateArea();

    public void display() { // Concrete method in abstract class
        System.out.println("A " + color + " shape with area: " + calculateArea());
    }
}

public interface Drawable {
    void draw();

    default void print() { // Default method (Java 8+)
        System.out.println("Printing shape...");
    }

    static void printInfo() { // Static method in interface
        System.out.println("Drawable interface info");
    }
}
```

**Composition over inheritance principle:**
```java
public class Car {
    private Engine engine;
    private Transmission transmission;
    private List<Wheel> wheels;

    public Car(Engine engine, Transmission transmission) {
        this.engine = engine;
        this.transmission = transmission;
        this.wheels = Arrays.asList(new Wheel(), new Wheel(), new Wheel(), new Wheel());
    }

    public void start() {
        engine.start();
        System.out.println("Car started");
    }
}
```

**Design patterns:**
- **Singleton**: Ensure only one instance exists
- **Factory**: Create objects without specifying exact classes
- **Observer**: Define one-to-many dependency between objects
- **Strategy**: Define family of algorithms, make them interchangeable
- **Builder**: Construct complex objects step by step

**Functional interfaces and lambda expressions:**
```java
@FunctionalInterface
public interface Calculator {
    int calculate(int a, int b);
}

Calculator add = (a, b) -> a + b;
Calculator multiply = (a, b) -> a * b;
```

Which advanced concept or design pattern interests you most?"""

    def _get_collections_response(self, user_level: str) -> str:
        """Collections and arrays by level"""
        if user_level == "beginner":
            return """Arrays and Lists store multiple values:

**Arrays (fixed size, fast access):**
```java
// Declaration and initialization
int[] numbers = {1, 2, 3, 4, 5};
String[] names = new String[3]; // Creates array of size 3

// Adding values to empty array
names[0] = "Alice";
names[1] = "Bob";
names[2] = "Charlie";

// Accessing values
System.out.println(numbers[0]);    // Prints: 1
System.out.println(names.length);  // Prints: 3
```

**ArrayList (dynamic size, flexible):**
```java
import java.util.ArrayList;

ArrayList<String> fruits = new ArrayList<>();
fruits.add("Apple");
fruits.add("Banana");
fruits.add("Orange");

System.out.println(fruits.get(0));  // Prints: Apple
System.out.println(fruits.size());  // Prints: 3

fruits.remove("Banana");
System.out.println(fruits.size());  // Prints: 2
```

**Looping through collections:**
```java
// Array
for (int number : numbers) {
    System.out.println(number);
}

// ArrayList
for (String fruit : fruits) {
    System.out.println(fruit);
}
```

Try creating an ArrayList of your favorite movies and displaying them!"""

        elif user_level == "intermediate":
            return """Java Collections Framework provides powerful data structures:

**List interface (ordered, allows duplicates):**
```java
List<String> arrayList = new ArrayList<>();    // Resizable array, fast random access
List<String> linkedList = new LinkedList<>();  // Double-linked list, fast insertions

arrayList.add("First");
arrayList.add(1, "Second"); // Insert at specific index
```

**Set interface (no duplicates):**
```java
Set<Integer> hashSet = new HashSet<>();     // Fast lookup, no order
Set<Integer> treeSet = new TreeSet<>();     // Sorted order, slower operations
Set<Integer> linkedHashSet = new LinkedHashSet<>(); // Insertion order maintained

hashSet.add(5);
hashSet.add(3);
hashSet.add(5); // Duplicate ignored
System.out.println(hashSet.size()); // Prints: 2
```

**Map interface (key-value pairs):**
```java
Map<String, Integer> ages = new HashMap<>();
ages.put("Alice", 25);
ages.put("Bob", 30);
ages.put("Charlie", 35);

System.out.println(ages.get("Alice")); // Prints: 25
System.out.println(ages.containsKey("Bob")); // Prints: true

// Iterating over maps
for (Map.Entry<String, Integer> entry : ages.entrySet()) {
    System.out.println(entry.getKey() + " is " + entry.getValue() + " years old");
}
```

**Common operations:**
```java
List<String> words = Arrays.asList("java", "python", "javascript", "c++");

// Filtering and transforming (Java 8+)
words.stream()
     .filter(word -> word.length() > 4)
     .map(String::toUpperCase)
     .forEach(System.out::println);
```

Which collection type fits your current problem?"""

        else:  # advanced
            return """Advanced collection patterns and performance optimization:

**Concurrent collections for thread safety:**
```java
ConcurrentHashMap<String, Integer> threadSafeMap = new ConcurrentHashMap<>();
CopyOnWriteArrayList<String> threadSafeList = new CopyOnWriteArrayList<>();
BlockingQueue<Task> taskQueue = new LinkedBlockingQueue<>();
```

**Custom collectors and advanced streams:**
```java
List<Person> people = getPersonList();

// Group by age
Map<Integer, List<Person>> byAge = people.stream()
    .collect(Collectors.groupingBy(Person::getAge));

// Custom collector
Collector<String, ?, String> joining = Collector.of(
    StringBuilder::new,
    StringBuilder::append,
    StringBuilder::append,
    StringBuilder::toString
);

// Parallel processing with careful consideration
List<String> results = largeDataSet.parallelStream()
    .filter(this::expensiveOperation)
    .collect(Collectors.toList());
```

**Performance characteristics:**
```java
// ArrayList vs LinkedList
// - ArrayList: O(1) random access, O(n) insertions in middle
// - LinkedList: O(n) random access, O(1) insertions anywhere

// HashMap vs TreeMap vs LinkedHashMap
// - HashMap: O(1) average operations, no ordering
// - TreeMap: O(log n) operations, sorted by keys
// - LinkedHashMap: O(1) operations, maintains insertion/access order
```

**Memory-efficient alternatives:**
```java
// For primitive collections (avoiding boxing overhead)
TIntList intList = new TIntArrayList(); // Trove library
IntList primitive = new IntArrayList(); // Eclipse Collections

// Immutable collections (Google Guava or Java 9+)
List<String> immutable = List.of("a", "b", "c");
Set<Integer> immutableSet = Set.of(1, 2, 3);
```

Need help with thread safety, performance optimization, or specific collection algorithms?"""

    def _get_conditions_response(self, user_level: str) -> str:
        """Conditional statements explanation"""
        return """Conditional statements control program flow based on conditions:

**Basic if-else statements:**
```java
int age = 18;
if (age >= 18) {
    System.out.println("You can vote!");
} else {
    System.out.println("Too young to vote.");
}
```

**Multiple conditions with else-if:**
```java
int score = 85;
if (score >= 90) {
    System.out.println("Grade: A");
} else if (score >= 80) {
    System.out.println("Grade: B");
} else if (score >= 70) {
    System.out.println("Grade: C");
} else if (score >= 60) {
    System.out.println("Grade: D");
} else {
    System.out.println("Grade: F");
}
```

**Switch statement (Java 7+ supports Strings):**
```java
String day = "Monday";
switch (day) {
    case "Monday":
        System.out.println("Start of work week");
        break;
    case "Tuesday":
    case "Wednesday":
    case "Thursday":
        System.out.println("Midweek");
        break;
    case "Friday":
        System.out.println("TGIF!");
        break;
    case "Saturday":
    case "Sunday":
        System.out.println("Weekend!");
        break;
    default:
        System.out.println("Invalid day");
}
```

**Ternary operator (compact if-else):**
```java
int age = 20;
String status = (age >= 18) ? "Adult" : "Minor";
System.out.println("Status: " + status);
```

**Logical operators:**
```java
boolean hasLicense = true;
int age = 20;

if (age >= 16 && hasLicense) {
    System.out.println("Can drive");
}

if (age < 13 || age > 65) {
    System.out.println("Discounted ticket");
}

if (!(age < 18)) { // Same as age >= 18
    System.out.println("Adult");
}
```

Try writing a program that determines if a year is a leap year!"""

    def _get_error_handling_response(self, user_level: str) -> str:
        """Error handling explanation by level"""
        if user_level == "beginner":
            return """Error handling helps your program deal with unexpected situations gracefully:

**Basic try-catch structure:**
```java
try {
    int result = 10 / 0; // This will cause ArithmeticException
    System.out.println("Result: " + result);
} catch (ArithmeticException e) {
    System.out.println("Error: Cannot divide by zero!");
}
```

**Multiple catch blocks:**
```java
try {
    int[] numbers = {1, 2, 3};
    System.out.println(numbers[5]); // ArrayIndexOutOfBoundsException

    String text = null;
    System.out.println(text.length()); // NullPointerException

} catch (ArrayIndexOutOfBoundsException e) {
    System.out.println("Error: Array index is out of bounds!");
} catch (NullPointerException e) {
    System.out.println("Error: Trying to use null object!");
} catch (Exception e) {
    System.out.println("Error: Something unexpected happened!");
}
```

**Finally block (always executes):**
```java
try {
    // Some risky code
    System.out.println("Executing risky code");
} catch (Exception e) {
    System.out.println("Caught exception: " + e.getMessage());
} finally {
    System.out.println("This always runs - cleanup code goes here");
}
```

**Common exceptions to handle:**
- `ArithmeticException`: Division by zero
- `ArrayIndexOutOfBoundsException`: Invalid array index
- `NullPointerException`: Using null reference
- `NumberFormatException`: Invalid number conversion

Always handle errors gracefully to make your programs more robust!"""

        else:
            return """Advanced error handling patterns and best practices:

**Try-with-resources (automatic resource management):**
```java
try (FileReader file = new FileReader("data.txt");
     BufferedReader buffer = new BufferedReader(file)) {

    String line;
    while ((line = buffer.readLine()) != null) {
        System.out.println(line);
    }
    // Resources automatically closed even if exception occurs

} catch (IOException e) {
    logger.error("File processing failed", e);
    throw new DataProcessingException("Cannot read configuration", e);
}
```

**Custom exceptions for domain-specific errors:**
```java
public class InsufficientFundsException extends Exception {
    private final double requestedAmount;
    private final double availableBalance;

    public InsufficientFundsException(double requested, double available) {
        super(String.format("Insufficient funds: requested %.2f, available %.2f", 
                           requested, available));
        this.requestedAmount = requested;
        this.availableBalance = available;
    }

    // Getters for additional context
    public double getRequestedAmount() { return requestedAmount; }
    public double getAvailableBalance() { return availableBalance; }
}
```

**Exception chaining and context:**
```java
public void processOrder(Order order) throws OrderProcessingException {
    try {
        validateInventory(order);
        chargePayment(order);
        shipOrder(order);
    } catch (InventoryException | PaymentException | ShippingException e) {
        // Chain exceptions to preserve stack trace
        throw new OrderProcessingException("Failed to process order: " + order.getId(), e);
    }
}
```

**Best practices:**
- Catch specific exceptions, not just `Exception`
- Use try-with-resources for any `AutoCloseable` resources
- Log errors with appropriate context
- Fail fast - validate inputs early
- Don't swallow exceptions silently
- Use checked exceptions for recoverable errors, unchecked for programming errors

**Modern alternatives (Optional for null safety):**
```java
Optional<User> user = userRepository.findById(userId);
return user.map(User::getEmail)
           .orElseThrow(() -> new UserNotFoundException("User not found: " + userId));
```

Which aspect of error handling would you like to explore further?"""

    def _get_io_response(self, user_level: str) -> str:
        """Input/Output operations explanation"""
        return """Input and output operations let your program interact with users and files:

**Reading user input with Scanner:**
```java
import java.util.Scanner;

Scanner scanner = new Scanner(System.in);

System.out.print("Enter your name: ");
String name = scanner.nextLine();

System.out.print("Enter your age: ");
int age = scanner.nextInt();

System.out.println("Hello " + name + ", you are " + age + " years old!");

scanner.close(); // Always close Scanner when done
```

**Different input methods:**
```java
Scanner scanner = new Scanner(System.in);

String line = scanner.nextLine();     // Read entire line
String word = scanner.next();         // Read next word
int number = scanner.nextInt();       // Read integer
double decimal = scanner.nextDouble(); // Read decimal number
boolean flag = scanner.nextBoolean();  // Read true/false
```

**Output formatting:**
```java
String name = "Alice";
int age = 25;
double height = 5.6;

// Basic output
System.out.println("Name: " + name);

// Formatted output (printf style)
System.out.printf("Name: %s, Age: %d, Height: %.1f feet%n", name, age, height);
```

**File operations (basic):**
```java
// Writing to a file
try {
    FileWriter writer = new FileWriter("output.txt");
    writer.write("Hello, World!");
    writer.close();
} catch (IOException e) {
    System.out.println("Error writing file: " + e.getMessage());
}

// Reading from a file
try {
    Scanner fileScanner = new Scanner(new File("input.txt"));
    while (fileScanner.hasNextLine()) {
        String line = fileScanner.nextLine();
        System.out.println(line);
    }
    fileScanner.close();
} catch (FileNotFoundException e) {
    System.out.println("File not found: " + e.getMessage());
}
```

Try creating a program that asks for user's favorite color and saves it to a file!"""

    def _get_exercise_response(self, user_level: str) -> str:
        """Generate exercise based on user level"""
        exercises = {
            "beginner": [
                "Create a program that calculates the area of a rectangle (length × width)",
                "Write a program that converts Celsius to Fahrenheit using the formula: F = C × 9/5 + 32",
                "Create a simple calculator that asks for two numbers and an operation (+, -, *, /)",
                "Write a program that finds the largest of three numbers using if-else statements",
                "Create a program that prints the multiplication table for a number entered by the user",
                "Write a program that counts how many vowels are in a word entered by the user"
            ],
            "intermediate": [
                "Create a Student class with methods to calculate GPA from a list of grades",
                "Implement a simple bank account system with deposit, withdraw, and balance inquiry",
                "Build a library system that manages books (add, remove, search by title/author)",
                "Create a shopping cart system with add/remove items and calculate total with tax",
                "Implement a simple inventory management system for a store",
                "Create a contact book that can add, delete, and search for contacts"
            ],
            "advanced": [
                "Implement a thread-safe cache using ConcurrentHashMap with expiration",
                "Create a REST API client that fetches and parses JSON data from a web service",
                "Build a simple web server using Java's built-in HTTP server",
                "Implement the Observer design pattern for a news subscription system",
                "Create a file compression utility using Java's built-in compression APIs",
                "Build a multi-threaded download manager that can download files in parallel"
            ]
        }

        selected_exercises = exercises.get(user_level, exercises["beginner"])
        exercise = random.choice(selected_exercises)

        return f"""Here's a coding exercise for your level ({user_level}):

**Challenge:** {exercise}

**Approach:**
1. Break the problem into smaller, manageable steps
2. Write pseudocode or plan your solution first
3. Start with a simple version, then add features
4. Test your code with different inputs
5. Handle edge cases and potential errors

**Tips for {user_level} level:**
{self._get_level_specific_tips(user_level)}

Show me your code when you're ready, and I'll provide feedback and suggestions for improvement!

Need help getting started or have questions about specific parts?"""

    def _get_level_specific_tips(self, user_level: str) -> str:
        """Get tips specific to user level"""
        tips = {
            "beginner": "- Focus on getting the basic logic working first\n- Use meaningful variable names\n- Don't forget to handle invalid input\n- Test with simple examples before complex ones",
            "intermediate": "- Think about class design and responsibilities\n- Use appropriate collections (ArrayList, HashMap, etc.)\n- Implement proper error handling\n- Consider code reusability and organization",
            "advanced": "- Consider performance and scalability\n- Think about thread safety if applicable\n- Use modern Java features (streams, lambdas)\n- Consider design patterns and architectural principles"
        }
        return tips.get(user_level, tips["beginner"])

    def _get_help_response(self, user_level: str) -> str:
        """Enhanced help response"""
        return f"""Hello! I'm JavaMentor, your assistant for learning Java programming.

**Your current level: {user_level}**

I can help you with:
- **Detailed explanations** of Java concepts with code examples
- **Interactive exercises** tailored to your skill level
- **Code review** and debugging assistance
- **Best practices** for writing clean, efficient Java code
- **Step-by-step guidance** through programming challenges

**Popular topics for {user_level} level:**
{self._get_level_topics(user_level)}

**How to get the best help:**
- Be specific about what you're trying to achieve
- Share your code if you're stuck on something
- Ask follow-up questions to dive deeper into topics
- Request exercises when you want to practice

What would you like to learn about today? I'm here to help you master Java programming!

(Note: OpenAI is not configured yet, I'm using pre-programmed responses)"""

    def _get_level_topics(self, user_level: str) -> str:
        """Get topics relevant to user level"""
        topics = {
            "beginner": "• Variables and data types (int, String, boolean, etc.)\n• Control structures (if-else, loops)\n• Basic input/output with Scanner\n• Simple methods and classes\n• Arrays and basic problem solving",
            "intermediate": "• Object-oriented programming (classes, inheritance, polymorphism)\n• Collections (ArrayList, HashMap, Set)\n• Exception handling and file I/O\n• String manipulation and regular expressions\n• Algorithm basics and data structures",
            "advanced": "• Stream API and functional programming\n• Multithreading and concurrency\n• Design patterns (Singleton, Factory, Observer)\n• Performance optimization and memory management\n• Integration with databases and web services"
        }
        return topics.get(user_level, topics["beginner"])

    def _get_default_response(self, original_message: str, user_level: str) -> str:
        """Enhanced default response with suggestions"""
        return f"""I'd be happy to help you with: "{original_message}"

As your JavaMentor for {user_level} level, I can provide detailed explanations and practical examples for any Java topic.

Could you be more specific about what you'd like to know? Here are some ways to ask:

**For concepts:**
- "How do I create a class in Java?"
- "What's the difference between ArrayList and LinkedList?"
- "Explain inheritance with an example"

**For problems:**
- "I'm getting a NullPointerException, how do I fix it?"
- "How do I read a file in Java?"
- "My loop isn't working as expected"

**For practice:**
- "Give me an exercise on {self._get_suggested_topic(user_level)}"
- "I want to practice object-oriented programming"
- "Can you review my code?"

I'm here to help you master Java programming step by step!

(Note: OpenAI is not configured yet, I'm using pre-programmed responses)"""

    def _get_suggested_topic(self, user_level: str) -> str:
        """Suggest a topic based on user level"""
        suggestions = {
            "beginner": "variables and loops",
            "intermediate": "classes and collections",
            "advanced": "design patterns or multithreading"
        }
        return suggestions.get(user_level, "variables")

    def generate_exercise(self, topic: str, difficulty: str) -> Dict:
        """Enhanced exercise generation with detailed solutions"""

        exercises_db = {
            "variables_beginner": {
                "title": "Personal Information Program",
                "description": "Create a program that stores and displays personal information using different variable types.",
                "requirements": [
                    "Declare variables for name (String), age (int), height (double), and student status (boolean)",
                    "Initialize each variable with appropriate values",
                    "Display the information in a formatted way",
                    "Calculate and display birth year based on current year and age"
                ],
                "starter_code": """public class PersonalInfo {
    public static void main(String[] args) {
        // TODO: Declare your variables here

        // TODO: Calculate birth year

        // TODO: Display the information

    }
}""",
                "solution": """public class PersonalInfo {
    public static void main(String[] args) {
        // Declare and initialize variables
        String name = "Alice Johnson";
        int age = 22;
        double height = 5.6;
        boolean isStudent = true;
        int currentYear = 2024;

        // Calculate birth year
        int birthYear = currentYear - age;

        // Display the information
        System.out.println("=== Personal Information ===");
        System.out.println("Name: " + name);
        System.out.println("Age: " + age + " years old");
        System.out.println("Height: " + height + " feet");
        System.out.println("Birth Year: " + birthYear);
        System.out.println("Student: " + (isStudent ? "Yes" : "No"));
    }
}""",
                "concepts": ["Variable declaration", "Data types", "Arithmetic operations", "String concatenation",
                             "Ternary operator"],
                "extension_ideas": [
                    "Add more personal details (email, phone number)",
                    "Calculate how many days until next birthday",
                    "Use Scanner to get input from user instead of hardcoded values"
                ]
            },

            "loops_beginner": {
                "title": "Number Pattern Generator",
                "description": "Create a program that generates different number patterns using various types of loops.",
                "requirements": [
                    "Use a for loop to print numbers 1 to 10",
                    "Use a while loop to print even numbers from 2 to 20",
                    "Create a nested loop to print a multiplication table",
                    "Add a do-while loop example"
                ],
                "starter_code": """public class NumberPatterns {
    public static void main(String[] args) {
        // TODO: Print numbers 1 to 10 using for loop

        // TODO: Print even numbers 2 to 20 using while loop

        // TODO: Print a 5x5 multiplication table using nested loops

        // TODO: Add a do-while loop example

    }
}""",
                "solution": """public class NumberPatterns {
    public static void main(String[] args) {
        // 1. Print numbers 1 to 10 using for loop
        System.out.println("Numbers 1 to 10:");
        for (int i = 1; i <= 10; i++) {
            System.out.print(i + " ");
        }
        System.out.println(); // New line

        // 2. Print even numbers 2 to 20 using while loop
        System.out.println("Even numbers 2 to 20:");
        int num = 2;
        while (num <= 20) {
            System.out.print(num + " ");
            num += 2; // Increment by 2 for even numbers
        }
        System.out.println(); // New line

        // 3. Print a 5x5 multiplication table using nested loops
        System.out.println("5x5 Multiplication Table:");
        for (int i = 1; i <= 5; i++) {
            for (int j = 1; j <= 5; j++) {
                System.out.printf("%4d", i * j); // Format with 4 spaces
            }
            System.out.println(); // New line after each row
        }

        // 4. Do-while loop example (always executes at least once)
        System.out.println("Countdown using do-while:");
        int countdown = 5;
        do {
            System.out.println(countdown);
            countdown--;
        } while (countdown > 0);
        System.out.println("Blast off!");
    }
}""",
                "concepts": ["For loops", "While loops", "Do-while loops", "Nested loops", "Loop control",
                             "Formatted output"],
                "extension_ideas": [
                    "Create a pattern that prints stars in a triangle shape",
                    "Generate the Fibonacci sequence using loops",
                    "Create an interactive program that asks user for the range of numbers"
                ]
            },

            "oop_intermediate": {
                "title": "Simple Banking System",
                "description": "Create a basic banking system demonstrating object-oriented programming principles.",
                "requirements": [
                    "Create a BankAccount class with private balance field",
                    "Implement deposit, withdraw, and getBalance methods",
                    "Add constructor to initialize account with initial balance",
                    "Include validation for negative amounts and insufficient funds",
                    "Create a main method to test the class"
                ],
                "starter_code": """public class BankAccount {
    // TODO: Add private fields

    // TODO: Add constructor

    // TODO: Add deposit method

    // TODO: Add withdraw method

    // TODO: Add getBalance method

    public static void main(String[] args) {
        // TODO: Test your BankAccount class

    }
}""",
                "solution": """public class BankAccount {
    private double balance;
    private String accountNumber;

    // Constructor
    public BankAccount(String accountNumber, double initialBalance) {
        this.accountNumber = accountNumber;
        this.balance = Math.max(0, initialBalance); // Ensure non-negative balance
    }

    // Deposit method
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.printf("Deposited $%.2f. New balance: $%.2f%n", amount, balance);
        } else {
            System.out.println("Deposit amount must be positive");
        }
    }

    // Withdraw method
    public boolean withdraw(double amount) {
        if (amount <= 0) {
            System.out.println("Withdrawal amount must be positive");
            return false;
        }

        if (amount > balance) {
            System.out.printf("Insufficient funds. Available: $%.2f%n", balance);
            return false;
        }

        balance -= amount;
        System.out.printf("Withdrew $%.2f. New balance: $%.2f%n", amount, balance);
        return true;
    }

    // Get balance method
    public double getBalance() {
        return balance;
    }

    // Get account number
    public String getAccountNumber() {
        return accountNumber;
    }

    public static void main(String[] args) {
        // Test the BankAccount class
        BankAccount account = new BankAccount("12345", 1000.0);

        System.out.println("Account: " + account.getAccountNumber());
        System.out.printf("Initial balance: $%.2f%n", account.getBalance());

        // Test deposit
        account.deposit(250.0);
        account.deposit(-50.0); // Should show error

        // Test withdraw
        account.withdraw(100.0);
        account.withdraw(2000.0); // Should show insufficient funds
        account.withdraw(-25.0);  // Should show error

        System.out.printf("Final balance: $%.2f%n", account.getBalance());
    }
}""",
                "concepts": ["Classes and objects", "Encapsulation", "Constructors",
                             "Method parameters and return values", "Input validation"],
                "extension_ideas": [
                    "Add transaction history using ArrayList",
                    "Create different account types (Checking, Savings) with inheritance",
                    "Add interest calculation for savings accounts",
                    "Implement account number generation"
                ]
            }
        }

        key = f"{topic}_{difficulty}"
        return exercises_db.get(key, exercises_db["variables_beginner"])