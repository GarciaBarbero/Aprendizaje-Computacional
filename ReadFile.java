import java.io.File;  // Import the File class
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.util.Scanner; // Import the Scanner class to read text files




public class ReadFile {
  public static void main(String[] args) {
    try {
      File myObj = new File("test.txt");
      Scanner myReader = new Scanner(myObj);
      Tablas tablas = new Tablas(myReader.nextLine(), ",");
      while (myReader.hasNextLine()) {
       tablas.setValue(myReader.nextLine(), false); 
      }
      System.out.println(tablas); 
      myReader.close();
    } catch (FileNotFoundException e) {
      System.out.println("An error occurred.");
      e.printStackTrace();
    }
  }
}
