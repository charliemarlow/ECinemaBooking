import java.util.Date;

public class CreditCard
{

    int creditCardID;
    String cardNumber;
    String cvv;
    Date expirationDate;
    int customerID;

    public CreditCard(int creditCardID, String cardNumber, String cvv, Date expirationDate, int customerID)
    {
	this.creditCardID = creditCardID;
	this.cardNumber = cardNumber;
	this.cvv = cvv;
	this.expirationDate = expirationDate;
	this.customerID = customerID;
    }//CreditCard

    public void changeCard(int creditCardID, String cardNumber, String cvv, Date expirationDate, int customerID)
    {
       	this.creditCardID = creditCardID;
	this.cardNumber = cardNumber;
	this.cvv = cvv;
	this.expirationDate = expirationDate;
	this.customerID = customerID;
    }//changeCard

    
}//CreditCard
