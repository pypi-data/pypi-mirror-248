//
// Created by jorge on 11/2/20.
//

#ifndef FTDCPARSER_FTDCPARSER_H
#define FTDCPARSER_FTDCPARSER_H

#define SPDLOG_ACTIVE_LEVEL SPDLOG_LEVEL_TRACE

#include <Dataset.h>
#include <ParserState.h>
#include "spdlog/spdlog.h"
#include <string_view>
#include <string>

// From libbson
#include <bson/bson.h>
#include <fstream>
#include "spdlog/logger.h"

class FTDCParser    {



public:
    FTDCParser();
    int  open(const std::string& file_path);
    bool close();
    int  read();
    int  parse();
    Dataset* readDataset(const std::string& file_path);
    int uncompressBlob(size_t i);
    size_t getBlobCount();
    int varint(int i);

    std::vector<Dataset *>parseFiles(const std::vector<std::string>& files);
    Dataset *parseFile(const std::string &file, bool single_threaded);
    std::vector<std::string> getMetricsNamesPrefixed(const std::string& prefix, Dataset *ds) ;
    std::vector<std::string> getMetricsNames(Dataset *ds);
    size_t dumpDocsAsJsonTimestamps( std::string  inputFile,  std::string  outputFile, ftdcparser::Timestamp start, ftdcparser::Timestamp end);
    size_t dumpDocsAsCsvTimestamps( std::string  inputFile,  std::string  outputFile, ftdcparser::Timestamp start, ftdcparser::Timestamp end);
    void setVerbose(bool verbosity);


    enum {
        statusOk = 0,
        statusFileNotFound = -1,
        statusFailedToOpen = -2,
        statusParserStateNull = -3,
        statusBlobIndexOutOfRange = -4,
    };

private:
    void visit_bson(const bson_t *bson, const size_t *length, void *data);


    std::shared_ptr<spdlog::logger> logger;
    bool verbose = false;

    bson_reader_t *reader{0};
    ParserState *parserState{0};
};

#endif //FTDCPARSER_FTDCPARSER_H