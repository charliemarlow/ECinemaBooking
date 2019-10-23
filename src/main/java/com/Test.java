package ecinema;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Date;

public class Test {
    public static void main(String[] args){
        System.out.println("Starting in Main");
        String first = "Jane";
        String last = "Doe";
        String password = "test1234";
        String confirmation = "test123";
        String email = "test@example.com";
        String username = "JaneDoeerryDay";
        boolean promotion = True;

        // Create dummy customer object
        Customer newCustomer = new Customer();

        // hash password
        password = newCustomer.hashPassword(password);

        // Validate the information
        boolean validated = false;
        while(!validated){
            if(!newCustomer.validateFirstName(first)){
                System.out.println("First name is wrong");
            }
            if(!newCustomer.validateLastName(last)){
                System.out.println("Last name is wrong");
            }
            //if(!validatePassword(password))
            if(!newCustomer.validateEmail(email)){
                System.out.println("Email is wrong");
            }
            if(!newCustomer.validateUsername(username)){
                System.out.println("Username is wrong");
            }
        }

        // Create a Customer
        newCustomer.updateInformation(first, last, email, password, username, promotion);
        // Print out info that goes in DB
        newCustomer.saveCustomer();

        // Send out confirmation email
        newCustomer.sendConfirmationEmail();
    }
}
