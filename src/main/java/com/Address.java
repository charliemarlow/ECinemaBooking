public class Address
{

    int addressID;
    String street;
    String city;
    String state;
    String zipCode;
    int customerID;

    public Address(int addressID, String street, String city, String state, String zipCode, int customerID)
    {

	this.addressID = addressID;
	this.street = street;
	this.city = city;
	this.state = state;
	this.zipCode = zipCode;
	this.customerID = customerID;
    }//Address

    public void setAddress(int addressID, String street, String city, String state, String zipCode, int customerID)
    {
       	this.addressID = addressID;
	this.street = street;
	this.city = city;
	this.state = state;
	this.zipCode = zipCode;
	this.customerID = customerID;
    }//setAddress
}//Address
