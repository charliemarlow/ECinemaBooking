package ecinema;

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
        this.password = password;
        this.username = username;
        this.status = Status.ACTIVE;
        this.subscribedToPromo = promotion;
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
			this.password = password;
			this.card = newCard;
			this.address = address;
		}

}
