using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace api
{

    class Program
    {
        public static void Main()
        {
            Console.Title = "API";

            Dictionary<string, string> Params = new Dictionary<string, string>()
            {
                {"", "" },
                {"", "" },
                {"", "" },
                {"", "" },
            };

            Console.WriteLine("sdfsdf");

            var answer = GetRequest("http://127.0.0.1:5000/bot_police", Params).Result;
            Console.WriteLine(answer.ToString());
            Console.ReadLine();
        }

        static async Task<HttpResponseMessage> GetRequest(string address, Dictionary<string, string> Params)
        {
            HttpClient client = new HttpClient();

            try
            {
                Uri uri = new Uri(address);
                FormUrlEncodedContent content = new FormUrlEncodedContent(Params);

                return await client.PostAsync(address, content);
            }
            catch (Exception x)
            {
                Console.WriteLine("ERROR " + x.ToString());
            }
            finally
            {
                client.Dispose();
            }

            return null;
        }
    }

}
