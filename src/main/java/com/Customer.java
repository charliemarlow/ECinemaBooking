package ecinema;

import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.Properties;
import javax.mail.*;
import javax.mail.internet.*;

public class Customer extends User{
		private int customerID;
		private String firstName;
		private String lastName;
		private String email;
		private Status status;
		private boolean subscribedToPromo;

		private CreditCard card;
		private Address address;

		public Customer(){
			customerID = 0;
			firstName = "";
			lastName = "";
			email = "noemail@fake.com";
			status = Status.ACTIVE;
			subscribedToPromo = false;
		}

		public Customer(int ID, String firstName, String lastName, String email, Status status, boolean subscribed){
			this.customerID = ID;
			this.firstName = firstName;
			this.lastName = lastName;
			this.email = email;
			this.status = status;
			this.subscribedToPromo = subscribed;
		}

    public void updateInformation(String firstName, String LastName, String email, String password, String username, boolean promotion ){
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.setPassword(password);
        this.userID = username;
        this.status = Status.ACTIVE;
        this.subscribedToPromo = promotion;
    }

    public void saveCustomer(){
        System.out.println("Saving customer to the DB");
    }

    public boolean validateName(String name){
        return (name.length() > 1 && name.length() < 100);
    }

    public boolean validatePassword(String password, String confirmation){
        return password.equals(confirmation) &&
               password.length() >= 8 &&
               password.matches(".*\\d.*");
    }

    public boolean validateEmail(String email){
        if(email == null){
            return false;
        }
        String emailRegex = "^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$";
        Pattern emailPattern = Pattern.compile(emailRegex);
        Matcher regexMatcher = emailPattern.matcher(email);
        return regexMatcher.matches();
    }

    public boolean validateUsername(String username){
        System.out.println("Checking that it is unique");
        return this.validateName(username);
    }

    public void sendConfirmationEmail(){
        Properties prop = new Properties();
        String user = "ecinemaBookingWebsite@gmail.com";
        String password = "4050Project";
        String host = "mail.gmail.com";

        prop.put("mail.smtp.host", host);
        prop.put("mail.smtp.auth", "true");

        Session session = Session.getDefaultInstance(prop, new javax.mail.Authenticator(){
                protected PasswordAuthentication getPasswordAuthentication(){
                    return new PasswordAuthentication(user, password);
                }
            });

        try {
            MimeMessage message = new MimeMessage(session);
            message.setFrom(new InternetAddress(user));
            message.addRecipient(Message.RecipientType.TO,
                                 new InternetAddress(this.email));

            message.setSubject("test");
            message.setText("Testing");

            Transport.send(message);
            System.out.println("Message sent");
        }catch(Exception e) {
            e.printStackTrace();
        }
    }

		// Getters and Setters
		public int getCustomerID(){
			return customerID;
		}
		public void setCustomerID(int ID){
			customerID = ID;
		}

		public String getFirstName(){
			return firstName;
		}
		public void setFirstName(String name){
			firstName = name;
		}

		public String getLastName(){
			return lastName;
		}
		public void setLastName(String name){
			lastName = name;
		}

		public String getEmail(){
			return email;
		}
		public void setEmail(String email){
			this.email = email;
		}

		public Status getStatus(){
			return status;
		}
		public void setStatus(Status status){
			this.status = status;
		}

		public boolean getSubcription(){
			return subscribedToPromo;
		}
		public void setSubcription(boolean subscribed){
			subscribedToPromo = subscribed;
		}

		public void addCard(CreditCard newCard){
			card = newCard;
		}
		public void editProfile(String firstName, String lastName, String password, CreditCard newCard, Address address){
			this.firstName = firstName;
			this.lastName = lastName;
      this.setPassword(password);
			this.card = newCard;
			this.address = address;
		}

}
