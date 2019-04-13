
namespace CSharPyExtension
{
    public unsafe static partial class CsBridge
    {
        public static unsafe double SquareNumber(double x)
        {
            if (x < 0)
                throw new System.Exception("Fails if x < 0.");
            return x * x;
        }

        public static unsafe void RandomString(ref string dst)
        {
            dst = "Français";
        }
    }
}
