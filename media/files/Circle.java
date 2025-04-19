public class Circle extends SimpleGeometricObject
{
	private double radius;

	public Circle() //default constructor 
	{
											//super();
											//System.out.println("Inside Circle constructor");
	}
	
	public Circle(double radius) //parameterized constructor 1
	{
		this.radius=radius;
		System.out.println("Inside Circle constructor");
		
	}
					//parameterized constructor 2
	public Circle(double radius, String color, boolean filled)
	{
		this.radius=radius;
		setColor(color); // How about this.color=color?
		setFilled(filled); // How about this.filled=filled?
		System.out.println("Inside Circle constructor");
	}
	
	//public methods
	public double getRadius()
	{
		return radius;
	}

	public void setRadius(double radius)
	{
		this.radius=radius;
	}

	public double getArea()
	{
		return radius*radius*Math.PI;
	}
	
	public double getDiameter()
	{
		return 2*radius;
	}

	public double getPerimeter()
	{
		return 2*Math.PI*radius;
	}

	public void printCircle()
	{
		System.out.print("The circle is created on "+getDateCreated());
		System.out.println(" and the radius is "+radius);
	}
	
	public String toString()
		{
			return super.toString()+"\n radius is "+radius;
			//return "radius is "+radius;
		}

	/*public static void Welcome()
	{
		System.out.println("Welcome to Circle class!");
	}*/	
}