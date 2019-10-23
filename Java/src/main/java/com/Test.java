package ecinema;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Date;

public class Test {

    // essentially all this code should go
    // into a controller class for registration
    public static void main(String[] args){
        System.out.println("Starting in Main");
        String first = "Jane";
        String last = "Doe";
        String password = "test123568";
        String confirmation = "test123568";
        String email = "charmarlw@gmail.com";
        String username = "JaneDoeerryDay";
        boolean promotion = true;

        // Create dummy customer object
        Customer newCustomer = new Customer();

        // Validate the information
        boolean validated = false;
        while(!validated){
            validated = true;
            if(!newCustomer.validateName(first)){
                System.out.println("First name is wrong");
                validated = false;
            }
            if(!newCustomer.validateName(last)){
                System.out.println("Last name is wrong");
                validated = false;
            }
            if(!newCustomer.validatePassword(password, confirmation)){
                System.out.println("password is wrong");
                validated = false;
            }
            if(!newCustomer.validateEmail(email)){
                System.out.println("Email is wrong");
                validated = false;
            }
            if(!newCustomer.validateUsername(username)){
                System.out.println("Username is wrong");
                validated = false;
            }
            // return here and serve up an error message
        }

        // hash password
        //        password = newCustomer.hashPassword(password);

        // Create a Customer
        newCustomer.updateInformation(first, last, email, password, username, promotion);

        // Print out info that goes in DB
        newCustomer.saveCustomer();

        // Send out confirmation email
        newCustomer.sendConfirmationEmail();

        // now send them to a confirmation page
    }
}
