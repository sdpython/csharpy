// See the LICENSE file in the project root for more information.

using System;
using System.IO;
using System.Text;


namespace DynamicCS
{
    /// <summary>
    /// Captures standard output and error.
    /// </summary>
    public class StdCapture: IDisposable
    {
        readonly StringBuilder sbout;
        readonly StringBuilder sberr;
        readonly TextWriter cur_out;
        readonly TextWriter cur_err;

        public string StdOut => sbout.ToString();
        public string StdErr => sberr.ToString();

        /// <summary>
        /// Starts capturing the standard output and error.
        /// </summary>
        public StdCapture()
        {
            sbout = new StringBuilder();
            sberr = new StringBuilder();
            var sout = new StringWriter(sbout);
            var serr = new StringWriter(sberr);
            cur_out = Console.Out;
            cur_err = Console.Error;
            Console.SetOut(sout);
            Console.SetError(serr);
        }

        /// <summary>
        /// Puts back the standard streams.
        /// </summary>
        public void Dispose()
        {
            Console.SetOut(cur_out);
            Console.SetError(cur_err);
        }
    }
}
