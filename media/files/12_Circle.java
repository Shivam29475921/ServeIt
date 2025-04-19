public class Circle
{
	private double radius=1; //Data Field (or) instance variable
	private static int numOfObjects=0; // static variable

	Circle() // Default constructor - methods of special type
	{     
		this(5.0);
		System.out.println("Inside default constructor"); 
		numOfObjects++; 

	}
	Circle(double newRadius) //Parameterized constructor
	{
		System.out.println("Inside parameterized constructor");
		radius=newRadius;
		numOfObjects++;
	}

	//Object Behavior (use of dot operator to call them)
	double getArea() 
	{
		return radius*radius*Math.PI;
	}
	double getPerimeter()
	{
		return 2*radius*Math.PI;
	}
	public double getRadius()
	{
		return radius;
	}
	public void setRadius(double radius)
	{
		this.radius = (radius>=0) ? radius:0;
	}
	public static int getNumOfObjects()
	{
		return numOfObjects;
	}
}




