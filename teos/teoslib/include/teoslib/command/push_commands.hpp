#pragma once

#include <vector>
#include <boost/algorithm/string.hpp>

#include <teoslib/config.h>
#include <teoslib/eos_interface.hpp>
#include <teoslib/command.hpp>

using namespace std;

extern const char* pushSubcommands;

namespace teos
{
  namespace command
  {
    /**
    Push a transaction with a single message
    */
    class PushAction : public TeosCommand
    {
    public:
      PushAction(string contractName, string action, string data,
          string permission = "",
          int expirationSec = 30, 
          bool skipSignature = false,
          bool dontBroadcast = false,
          bool forceUnique = false )
      {
        copy(pushAction(
          contractName, action, data,
          permission,          
          expirationSec,
          skipSignature, dontBroadcast, forceUnique));
      }

      PushAction(ptree reqJson, bool raw = false) : TeosCommand(
        "", reqJson)
      {
        copy(pushAction(
          reqJson.get<string>("contract"), reqJson.get<string>("action"), 
          reqJson.get<string>("data"),
          reqJson.get<string>("permission"), 
          reqJson.get<int>("expiration"),          
          reqJson.get<bool>("skip"),
          reqJson.get<bool>("dontBroadcast"),
          reqJson.get<bool>("forceUnique")
          ));
      }
    };

    /**
    * @brief Command-line driver for the PushAction class.
    */
    class PushActionOptions : public CommandOptions
    {
    public:
      PushActionOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Push a transaction with a single message.
Usage: ./teos push message [contract] [action] [data] [scope] [permission] [Options]
Usage: ./teos create key [-j '{
  "contract":"<contract name>",
  "action":"<action on contract>",
  "data":"<json tree>",
  "scope":"<account list>",
  "permission":"<accountName@permitionLevel,accountName@permitionLevel>"
  "expiration":<expiration time sec>,  
  "skipSignature":<true|false>,
  "dontBroadcast":<true|false>,
  "forceUnique":<true|false>
  }'] [OPTIONS]
)EOF";
      }

      string contract;
      string action;
      string data;
      string permission;
      int expiration;      
      bool skip;
      bool dontBroadcast;
      bool forceUnique;

      options_description  argumentDescription() {
        options_description od("");
        od.add_options()
          ("contract,c", value<string>(&contract), "The account providing the contract to execute")
          ("action,a", value<string>(&action), "The action to execute on the contract")
          ("data,d", value<string>(&data), "The arguments to the contract")
          ("permission,p", value<string>(&permission)
            ->default_value("")
            ,"An account and permission level to authorize, as in "
            "'account@permission'")
          ("expiration,x", value<int>(&expiration)->default_value(30)
            , "The time in seconds before a transaction expires")
          ("skip,s", value<bool>(&skip)->default_value(false)
            , "Specify that unlocked wallet keys should not be used to sign "
            "transaction, defaults to false")
          ("dont-broadcast,d", value<bool>(&dontBroadcast)->default_value(false)
            , "Don't broadcast transaction to the network (just print to stdout)");
          ("force-unique,f", value<bool>(&forceUnique)->default_value(false)
            , "force the transaction to be unique. this will consume extra "
            "bandwidth and remove any protections against accidently issuing "
            "the same transaction multiple times"); 
        return od;
      }

      void setPosDesc(positional_options_description& pos_desc) {
        pos_desc.add("contract", 1);
        pos_desc.add("action", 1);
        pos_desc.add("data", 1);
        pos_desc.add("scope", 1);
        pos_desc.add("permission", 1);
      }

      bool checkArguments(variables_map &vm) {
        bool ok = false;
        if (vm.count("contract")) {
          reqJson_.put("contract", contract);
          if (vm.count("action")) {
            reqJson_.put("action", action);
            ok = true;
            if (vm.count("data")){
              reqJson_.put("data", data);
              reqJson_.put("permission", permission);
              reqJson_.put("expiration", expiration);                
              reqJson_.put("skip", skip);
              reqJson_.put("dontBroadcast", dontBroadcast);
              reqJson_.put("forceUnique", forceUnique);
            }
          }
        }
        return ok;
      }

      TeosControl executeCommand() {
        return PushAction(reqJson_);
      }

    };
  }
}